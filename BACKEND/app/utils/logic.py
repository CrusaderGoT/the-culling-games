from fastapi import Path, HTTPException, status
from typing import Annotated, Literal, Sequence
from email_validator import validate_email, EmailNotValidError
from app.utils.config import UserException
from app.utils.dependencies import session, atp
from sqlmodel import Session, and_, not_, select, exists
from random import sample, choice
from datetime import datetime, timedelta
import time
from app.models.barrier import BarrierRecord, BarrierTech
from app.models.match import Match, MatchPlayerLink, Vote
from ..models.colony import Colony
from app.models.user import User
from ..models.player import Player


def usernamedb(username: str):
    'returns the username as stored in the DB -> lowercase'
    return username.lower().strip()


def is_valid_email(email: str) -> bool:
    'checks if a string is a valid email string'
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def get_match(session: session, match_id: int):
    'function for getting a match via its ID.'
    match = session.exec(
        select(Match).where(Match.id == match_id)
    ).first()
    return match

def get_user(session: session, user_name_id_email: str | int):
    '''gets a user (using id, username, or email) from the database or returns none if user not found.
    \nuser_name_id_email: `username`, `userid`, or `email`'''
    # try to convert the str to int for id
    try:
        user_id = int(user_name_id_email)
    except ValueError:
        pass
    else:
        user_name_id_email = user_id

    if isinstance(user_name_id_email, str):
        # check if it is an email str
        if is_valid_email(user_name_id_email):
            statement = select(User).where(User.email == user_name_id_email)
            user = session.exec(statement=statement).first()
            return user
        else: # a username then
            username = usernamedb(user_name_id_email)
            statement = select(User).where(User.usernamedb == username)
            user = session.exec(statement=statement).first()
            return user
    elif isinstance(user_name_id_email, int):
        user = session.get(User, user_name_id_email)
        return user
    else:
        return None
    
def get_player(session: session, player_id: int):
    'for getting a player from the database'
    player = session.get(Player, player_id)
    if player:
        return player
    else:
        return None

def get_players_not_in_part(colony_id: int, part: int, session: Session):
    """
    Fetch players from a specified colony who haven't fought in a match for the given part.
    """
    # Subquery to get player IDs who have fought in the specified part
    part_matches_subquery = (
        select(MatchPlayerLink.player_id)
        .join(Match, MatchPlayerLink.match_id == Match.id)
        .where(Match.id == part) 
    ).subquery()

    part_matches_select = select(part_matches_subquery.c.player_id)

    # Query to get players in the specified colony who haven't fought in the part
    players_not_in_part_query = (
        select(Player)
        .where(
            and_(
                Player.colony_id == colony_id,
                not_(Player.id.in_(part_matches_select))
            )
        )
    )

    players_not_in_part = session.exec(players_not_in_part_query).all()

    return players_not_in_part

def select_players_fought_in_part(part: int):
        '''Subquery to get player IDs who have fought in the specified part\n
        returns a select statement'''
        subquery = (
            select(MatchPlayerLink.player_id)
            .join(Match, MatchPlayerLink.match_id == Match.id)
            .where(Match.part == part)
        ).subquery(name=f"matches_in_part_{part}")
        # Convert the subquery into a select() construct for use in the IN clause
        subquery_select = select(subquery.c.player_id)
        return subquery_select

def colonies_with_players_available_for_part(session: session, part: int):
    "Main query to get colonies IDs with at least one player who hasn't fought in the specified part"
    subquery_select = select_players_fought_in_part(part=part)
    statement = select(Colony.id).where(
        exists(
            select(Player.id)
            .where(
                and_(
                    Player.colony_id == Colony.id,
                    not_(Player.id.in_(subquery_select))
                )
            )
        )
    )
    result = session.exec(statement).all()
    return result


id_name_email = Annotated[int | str, Path(description="The user's Id, Username, or Email")]
"""The user's Id, Username, or Email as a Path parameter.
\nActually accepts any int or str. The name is for convention."""

def ongoing_match(match: Match):
    'checks if a match is still ongoing, returns false if match is over, otherwise true'
    time_now = datetime.now()
    end_time = match.end
    ongoing = time_now < end_time
    return ongoing


def points_required_for_upgrade(grade: Player.Grade):
    'returns the points required for an upgrade'
    points_dict = dict(
        [
            (4, 0.2),
            (3, 0.2),
            (2, 0.4),
            (1, 0.4),
            (0, 0.6),
        ]
    )
    return points_dict[grade.value]

def get_last_created_match(session: session):
    'Get the last created Match, according to begin date. None if no Match exists'
    last_match = session.exec(
        select(Match).order_by(Match.begin.desc())
        .limit(1)
    ).first()
    return last_match

def create_new_match(session: session, part: int, atp: atp):
    'creates a new match'
    # fetch colonies that has atleast one player that hasn't fought in the specified part query
    result = colonies_with_players_available_for_part(session, part)
    if result and (colony_id := choice(result)) is not None: # list is not empty and contains int (randomly chosen)
        # Fetch players from the selected colony who have not fought in the specified part.
        players_not_in_part = get_players_not_in_part(colony_id, part, session)
        # Randomly select 2 players from the colony for the match
        players = random_players_for_match(session, players_not_in_part, colony_id) 
        # create match
        begin = datetime.now() + atp.delay_begin_match # match begins in timedelta
        end = begin + atp.match_duration # match ends in timedelta 
        new_match = Match(begin=begin, end=end, part=part,
                        colony_id=colony_id, players=players)
        return new_match
    else:
        detail=f"No colony with players who haven't fought in part {part}. Begin/Try part {part+1}. Else no player yet..."
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=detail)
    
def random_players_for_match(session: session, players_not_in_part: Sequence[Player], colony_id: int):
    """Randomly select 2 players from the colony who haven't fought in the part before.\n
    if only one player is available, pair them with any other player from the colony.\n
    raises HTTPException if only one player in colony"""
    if len(players_not_in_part) == 1:
        # fetch all players in colony, excluding the single player_not in_part
        all_players_query = select(Player).where(Player.colony_id == colony_id, Player.id != players_not_in_part[0].id)
        all_players = session.exec(all_players_query).all()
        
        if not all_players: # means only one player in colony
            err_msg = f"Only one player in Colony {players_not_in_part[0].colony_id}, cannot make match. Try again or add a player to the colony"
            raise HTTPException(status.HTTP_412_PRECONDITION_FAILED, err_msg)
        else:
            player1 = players_not_in_part[0] # the only player available
            player2 = choice(all_players)  # Randomly select another player from the same colony

    else: # players available are more than 2
        # Randomly select two unique players from those who haven't fought in the specified part
        player1, player2 = sample(players_not_in_part, 2)
    return [player1, player2]

def calculate_points(player_points: float, points_to_action: float, on_action: Literal["minus", "plus"]):
    '''
    Calculates the point needed for a player action\n
    raises a `HTTPException 428` if player points are not enough.\n
    returns a 1 decimal place | 2 precision of a float. e.g. 1.2
    '''
    # check if player points is enough
    if player_points >= points_to_action: # player has enough points
        # check which action to perform
        match on_action:
            case "plus":
                updated_points = round(player_points + points_to_action, 1)
            case "minus":
                updated_points = round(player_points - points_to_action, 1)
            case _:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "points error occured.")
        return updated_points
    else:
        msg = f"not enough points; need {points_to_action}, have {player_points}"
        raise HTTPException(status.HTTP_428_PRECONDITION_REQUIRED, detail=msg)

def activate_domain(
        barrier_tech: BarrierTech,
        barrier_record: BarrierRecord | None,
        match: Match,
        session: session,
        atp: atp
    ):
    'function for activating a domain'
    # activate domain
    barrier_tech.domain_expansion = True
    # set deactivation time
    barrier_tech.de_end_time = datetime.now() + atp.domain_duration
    # deduct points
    barrier_tech.player.points = calculate_points(barrier_tech.player.points, atp.cost_domain_expansion, "minus")
    # add/record the detail
    # the barrier detail should commited here
    if barrier_record is not None:
        barrier_record.domain_counter += 1
        session.add(barrier_record)
    else: # no barrier detail
        new_barrier_detail = BarrierRecord(
            domain_counter=1,
            match=match,
            barrier_tech=barrier_tech
        )
        session.add(new_barrier_detail)
    # commits
    session.add(barrier_tech)
    session.commit()
    session.refresh(barrier_tech)
    return  barrier_tech

def deactivate_domain(barrier_tech: BarrierTech, session: session):
    'function for the background task of deactivating a domain'
    active = True
    while active:
        now = datetime.now() # the current time
        # check if there is no end time for the specified barrier tech DE
        if barrier_tech.de_end_time is None:
            # deactivate domain
            barrier_tech.de_end_time = None
            barrier_tech.domain_expansion = False
            session.add(barrier_tech)
            session.commit()
            active = False
            break
        # see if time for deactivation has reached
        elif now >= barrier_tech.de_end_time:
            # deactivate domain
            barrier_tech.de_end_time = None
            barrier_tech.domain_expansion = False
            session.add(barrier_tech)
            session.commit()
            active = False
            break
        else:
            # add a time pause if deactivation time is still further
            remaining_time = (barrier_tech.de_end_time - now).total_seconds()
            if remaining_time < 0:
                continue # loop here to avoid negative float being supplied to time.sleep
            time.sleep(remaining_time // 2) # remaining time divide by 2
            continue # loop again

def get_vote_point(
        match:Match, prev_votes: Sequence[Vote],
        player_bt: BarrierTech | None,
        opposing_player_bt: BarrierTech | None,
        atp: atp
    ) -> float:
    'vote function for getting the vote point of a particular vote'

    vote_point = atp.vote_point
    # OPTIONS CONTROL FLOW if/if/...
    # 1. limit vote of player with an active binding vow to three, for as long as it is active
    if (player_bt
        and player_bt.binding_vow == True
        and len(prev_votes) >= (limit := atp.vote_binding_vow_limit)
    ):
        raise HTTPException(status.HTTP_425_TOO_EARLY, f"binding vow active, cannot vote more than {limit} times")

    # 2. check if a player previously activated a binding vow that has paid off, in this match
    # then increment the vote_point, even if other BTs are active, except binding vow BT
    if (# this confirms a player has a BT, then confirms that the/a BT has been used in this match
        player_bt and match.barrier_records
        # it then tries to get the acculamted binding vow points of the player, if any
        and (binded_vow := [br.binding_vow_counter for br in match.barrier_records
                                if br.barrier_tech_id == player_bt.id])
        # finally checks that the player isn't currently under a binding vow
        and player_bt.binding_vow == False
    ):
        # ALL THESE CLAUSES MUST BE MET, HENCE THE 'and' OPERATORS.
        vote_point += binded_vow[0] # increase vote_point by binding vow accumulated points

    # STRICT CONTROL FLOW if/elif/else; only one of them runs
    # 3. check if domain is activated and p2 simple domain isn't activated
    if (# confirm the player has a barrier technique
        player_bt
        # then confirm that their DE is active
        and player_bt.domain_expansion == True
    ):
        # Now check if opposing player has a barrier tech of their own
        if (opposing_player_bt
            # check if their simple domain is active
            and opposing_player_bt.simple_domain == True
        ):
            # players DE effect is reduced by half if so
            vote_point *= atp.domain_expansion_point / 2
        else: # opposing player doesn't have an activated simple domain
            vote_point *= atp.domain_expansion_point # increase vote points

    # 4. Check if the opposing player has an active simple domain, outside of defending a DE
    # no need to check if player has their DE deactivated, since the above CONTROL FLOW
    # would have run, skipping this one; for this one to run implies player no DE or BT.
    elif (# check if opposing player has a barrier tech
        opposing_player_bt
        # and their simple domain is activated
        and opposing_player_bt.simple_domain == True):
        # if opponents simple domain is active, reduce vote points
        vote_point /= atp.simple_domain_point
    # 5. else no BT shenanigans
    else:
        vote_point = vote_point

    return round(vote_point, 1)


def conditions_for_barrier_tech(session:session, player_id: int, match_id: int,
                               player: Player | None, match: Match | None,
                               current_user: User):
    '''
    function for meeting the conditions nesseccary for the use of a barrier tech.
    i.e, check if player has a barrier technique.\n
    Otherwise raise a `HTTPException` error.\n
    Conditions:\n\t
    * match must exist
    * player must exist
    * player must have a barrier technique; player of grade 2 up
    \nreturns a tuple of `BarrierTech`, `BarrierRecord` if any, the `Match` the `BarrierTech` will be used in, and `Player`.
    '''
    if player is not None:
        if match is not None:
            if player.user_id != current_user.id:
                msg = f"cannot activate simple domain of another player"
                raise UserException(current_user, status.HTTP_406_NOT_ACCEPTABLE, msg)
            else:
                if ongoing_match(match) == True:
                    # check if domain has been actvated before
                    # get the Barrier technique of that player for the match
                    stmt = (
                        select(BarrierTech)
                        .join(Player)
                        .where(BarrierTech.player_id == player.id)
                    )
                    barrier_tech = session.exec(stmt).first()

                    # get the barrier details of the player for this match
                    bt_id = barrier_tech.id if barrier_tech else None # the barrier tech ID, else None

                    st = (
                        select(BarrierRecord)
                        .join(BarrierTech)
                        .join(Match)
                        .where(BarrierRecord.barrier_tech_id == bt_id)
                        .where(BarrierRecord.match_id == match.id)
                    )
                    barrier_record = session.exec(st).first()

                    if barrier_tech is None: # player has no barrier technique
                        msg = f"'{player.name}' doesn't have a barrier technique, upgrade the player to grade 2, to unlock Barrier Techniques"
                        raise HTTPException(status.HTTP_428_PRECONDITION_REQUIRED, msg)
                    else: # return the barrier tech and  barrier record if any
                        return barrier_tech, barrier_record, match, player

                else: # match has ended
                    raise HTTPException(status.HTTP_423_LOCKED, f"Match ID: {match_id}, has Ended")

        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Match ID: {match_id}, does not exist.")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Player {player_id}, does not exist.")
    
def activate_simple_domain(
        barrier_tech: BarrierTech,
        barrier_record: BarrierRecord | None,
        match, session: session,
        atp: atp
    ):
    # activate simple domain
    barrier_tech.simple_domain = True
    # set deactivation time
    barrier_tech.sd_end_time = datetime.now() + atp.simple_domain_duration
    # deduct points
    barrier_tech.player.points = calculate_points(barrier_tech.player.points, atp.cost_simple_domain, "minus")
    # add/record the detail
    # the barrier detail should commited here
    if barrier_record is not None:
        barrier_record.simple_domain_counter += 1
        session.add(barrier_record)
    else: # no barrier detail
        new_barrier_detail = BarrierRecord(
            simple_domain_counter=1,
            match=match,
            barrier_tech=barrier_tech
        )
        session.add(new_barrier_detail)
    # commits
    session.add(barrier_tech)
    session.commit()
    session.refresh(barrier_tech)
    return barrier_tech

def deactivate_simple_domain(barrier_tech: BarrierTech, session: session):
    'function for the background task of deactivating a simple domain'
    active = True
    while active:
        now = datetime.now() # the current time
        # check if there is no end time for the specified barrier tech SD
        if barrier_tech.sd_end_time is None:
            # deactivate simple domain
            barrier_tech.sd_end_time = None
            barrier_tech.simple_domain = False
            session.add(barrier_tech)
            session.commit()
            active = False
            break
        # see if time for deactivation has reached
        elif now >= barrier_tech.sd_end_time:
            # deactivate domain
            barrier_tech.de_end_time = None
            barrier_tech.domain_expansion = False
            session.add(barrier_tech)
            session.commit()
            active = False
            break
        else:
            # add a time pause if deactivation time is still further
            remaining_time = (barrier_tech.sd_end_time - now).total_seconds()
            if remaining_time < 0:
                continue # loop here to avoid negative float being supplied to time.sleep

            time.sleep(remaining_time // 2) # remaining time divide by 2
            continue # loop again

def activate_barrier_tech(technique: Literal["domain_expansion", "simple_domain", "binding_vow"],
                      barrier_tech: BarrierTech, barrier_record: BarrierRecord | None, match: Match,
                      session: session, atp: atp):
    'function for a match/case implementation of barrier techniques'    
    # make the variables depending on which technique to activate
    match technique:
        case "simple_domain":
            activate_simple_domain(barrier_tech, barrier_record, match, session, atp)
        case "domain_expansion":
            activate_domain(barrier_tech, barrier_record, match, session, atp)
        case "simple_domain":
            activate_simple_domain(barrier_tech, barrier_record, match, session, atp)


def assign_match_winner(*, match_id: int, session: session, atp: atp):
    'for assigning the winner of a match, after it ends'
    match = get_match(session=session, match_id=match_id)
    if match == None: # match doesn't exit
        return
    # check if match is ongoing
    active = ongoing_match(match)
    print (active, 'hereeeeeeeeee')
    while active:
        # pause the loop for 1/2 the time remaining
        now = datetime.now() # the current time
        half_time_remaining = (match.end - now).total_seconds() // 2
        if half_time_remaining < 0: # to avoid negative float being supplied to time.sleep
            active = False
            continue # last begin loop
        time.sleep(half_time_remaining)
        continue # run loop again after sleep
        
    else: # runs after the match is ended
        # get the total vote points of the players
        player_votes: dict[int, int] = dict()
        if len(match.votes) >= 1: # at least one vote
            for player in match.players:
                player_votes.setdefault(player.id, 0)
                for vote in match.votes:
                    if vote.player_id == player.id:
                        player_votes[player.id] += vote.point
            else: # runs after loop
                winner_key = max(player_votes, key= lambda k: player_votes[k])
                loser_key  = min(player_votes, key= lambda k: player_votes[k])
                # make sure it isn't a draw; if draw return/end code here
                if player_votes[winner_key] == player_votes[loser_key]:
                    return
                
                # assign winner extra 5 points
                winner = get_player(session=session, player_id=winner_key)
                if winner is None:
                    return
                winner.points += atp.winner_point
                match.winner = winner
                session.add(match)
                session.commit()
        else: # no vote was casted for this match
            # implement draw logic
            pass