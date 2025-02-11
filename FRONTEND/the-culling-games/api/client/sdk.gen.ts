// This file is auto-generated by @hey-api/openapi-ts

import { type Options as ClientOptions, type TDataShape, type Client, urlSearchParamsBodySerializer } from '@hey-api/client-next';
import type { CurrentUserData, CurrentUserResponse, AuserData, AuserResponse, AuserError, EditUserData, EditUserResponse, EditUserError, DeleteUserData, DeleteUserResponse, DeleteUserError, CreatePlayerData, CreatePlayerResponse, CreatePlayerError, MyPlayerData, MyPlayerResponse, GetPlayersData, GetPlayersResponse, GetPlayersError, APlayerData, APlayerResponse, APlayerError, EditPlayerData, EditPlayerResponse, EditPlayerError, DeletePlayerData, DeletePlayerResponse, DeletePlayerError, UpgradePlayerData, UpgradePlayerResponse, UpgradePlayerError, CreateMatchData, CreateMatchResponse, CreateMatchError, GetMatchesData, GetMatchesResponse, GetMatchesError, GetLastestMatchData, GetLastestMatchResponse, GetLastestMatchError, VoteData, VoteResponse, VoteError, DomainExpansionData, DomainExpansionResponse, DomainExpansionError, SimpleDomainData, SimpleDomainResponse, SimpleDomainError, CreateAdminData, CreateAdminResponse, CreateAdminError, NewPermissionData, NewPermissionResponse, NewPermissionError, DemoSuperuserData, DemoSuperuserError, CreateTokenData, CreateTokenResponse, CreateTokenError, CreateUserData, CreateUserResponse, CreateUserError } from './types.gen';
import { currentUserResponseTransformer, aUserResponseTransformer, editUserResponseTransformer, deleteUserResponseTransformer, createPlayerResponseTransformer, myPlayerResponseTransformer, aPlayerResponseTransformer, editPlayerResponseTransformer, deletePlayerResponseTransformer, upgradePlayerResponseTransformer, createMatchResponseTransformer, getMatchesResponseTransformer, getLastestMatchResponseTransformer, domainExpansionResponseTransformer, simpleDomainResponseTransformer, createAdminResponseTransformer, createUserResponseTransformer } from './transformers.gen';
import { zCurrentUserResponse, zAUserResponse, zEditUserResponse, zDeleteUserResponse, zCreatePlayerResponse, zMyPlayerResponse, zGetPlayersResponse, zAPlayerResponse, zEditPlayerResponse, zDeletePlayerResponse, zUpgradePlayerResponse, zCreateMatchResponse, zGetMatchesResponse, zGetLastestMatchResponse, zVoteResponse, zDomainExpansionResponse, zSimpleDomainResponse, zCreateAdminResponse, zNewPermissionResponse, zCreateTokenResponse, zCreateUserResponse } from './zod.gen';
import { client as _heyApiClient } from './client.gen';

export type Options<TData extends TDataShape = TDataShape, ThrowOnError extends boolean = boolean> = ClientOptions<TData, ThrowOnError> & {
    /**
     * You can provide a client instance returned by `createClient()` instead of
     * individual options. This might be also useful if you want to implement a
     * custom client.
     */
    client?: Client;
};

export class UsersService {
    /**
     * Get the logged in user
     */
    public static currentUser<ThrowOnError extends boolean = false>(options?: Options<CurrentUserData, ThrowOnError>) {
        return (options?.client ?? _heyApiClient).get<CurrentUserResponse, unknown, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: currentUserResponseTransformer,
            responseValidator: async (data) => {
                return await zCurrentUserResponse.parseAsync(data);
            },
            url: '/users/me',
            ...options
        });
    }
    
    /**
     * Get a user.
     */
    public static aUser<ThrowOnError extends boolean = false>(options: Options<AuserData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).get<AuserResponse, AuserError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: aUserResponseTransformer,
            responseValidator: async (data) => {
                return await zAUserResponse.parseAsync(data);
            },
            url: '/users/{user}',
            ...options
        });
    }
    
    /**
     * Edit a user.
     */
    public static editUser<ThrowOnError extends boolean = false>(options: Options<EditUserData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).patch<EditUserResponse, EditUserError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: editUserResponseTransformer,
            responseValidator: async (data) => {
                return await zEditUserResponse.parseAsync(data);
            },
            url: '/users/edit/{user}',
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers
            }
        });
    }
    
    /**
     * Delete a user.
     * Deleting a user will _set null_ on the *player* if any.
     */
    public static deleteUser<ThrowOnError extends boolean = false>(options: Options<DeleteUserData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).delete<DeleteUserResponse, DeleteUserError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: deleteUserResponseTransformer,
            responseValidator: async (data) => {
                return await zDeleteUserResponse.parseAsync(data);
            },
            url: '/users/delete/{user}',
            ...options
        });
    }
    
    /**
     * Create a new User
     */
    public static createUser<ThrowOnError extends boolean = false>(options: Options<CreateUserData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<CreateUserResponse, CreateUserError, ThrowOnError>({
            responseTransformer: createUserResponseTransformer,
            responseValidator: async (data) => {
                return await zCreateUserResponse.parseAsync(data);
            },
            url: '/signup',
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers
            }
        });
    }
    
}

export class PlayersService {
    /**
     * Create a new player
     */
    public static createPlayer<ThrowOnError extends boolean = false>(options: Options<CreatePlayerData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<CreatePlayerResponse, CreatePlayerError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: createPlayerResponseTransformer,
            responseValidator: async (data) => {
                return await zCreatePlayerResponse.parseAsync(data);
            },
            url: '/player/create/{user}',
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers
            }
        });
    }
    
    /**
     * Get a player of the logged in user
     */
    public static myPlayer<ThrowOnError extends boolean = false>(options?: Options<MyPlayerData, ThrowOnError>) {
        return (options?.client ?? _heyApiClient).get<MyPlayerResponse, unknown, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: myPlayerResponseTransformer,
            responseValidator: async (data) => {
                return await zMyPlayerResponse.parseAsync(data);
            },
            url: '/player/me',
            ...options
        });
    }
    
    /**
     * Get a list of players.
     */
    public static getPlayers<ThrowOnError extends boolean = false>(options?: Options<GetPlayersData, ThrowOnError>) {
        return (options?.client ?? _heyApiClient).get<GetPlayersResponse, GetPlayersError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseValidator: async (data) => {
                return await zGetPlayersResponse.parseAsync(data);
            },
            url: '/player/all',
            ...options
        });
    }
    
    /**
     * Get a player with their ID
     */
    public static aPlayer<ThrowOnError extends boolean = false>(options: Options<APlayerData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).get<APlayerResponse, APlayerError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: aPlayerResponseTransformer,
            responseValidator: async (data) => {
                return await zAPlayerResponse.parseAsync(data);
            },
            url: '/player/{player_id}',
            ...options
        });
    }
    
    /**
     * Edit a player details.
     * If an application is sent, it should have a valid number for the application you want to edit.
     *
     * To check an application number, first get a player info using the **'/players/{player_id}'** request.
     *
     * Else the application will be disregarded, valid numbers are 1-5.
     */
    public static editPlayer<ThrowOnError extends boolean = false>(options: Options<EditPlayerData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).patch<EditPlayerResponse, EditPlayerError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: editPlayerResponseTransformer,
            responseValidator: async (data) => {
                return await zEditPlayerResponse.parseAsync(data);
            },
            url: '/player/edit/{player_id}',
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers
            }
        });
    }
    
    /**
     * Delete a player
     */
    public static deletePlayer<ThrowOnError extends boolean = false>(options: Options<DeletePlayerData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).delete<DeletePlayerResponse, DeletePlayerError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: deletePlayerResponseTransformer,
            responseValidator: async (data) => {
                return await zDeletePlayerResponse.parseAsync(data);
            },
            url: '/player/delete/{player_id}',
            ...options
        });
    }
    
    /**
     * Upgrade Player
     * function for uprading the grade of a player.
     *
     * **points required.**
     */
    public static upgradePlayer<ThrowOnError extends boolean = false>(options: Options<UpgradePlayerData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<UpgradePlayerResponse, UpgradePlayerError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: upgradePlayerResponseTransformer,
            responseValidator: async (data) => {
                return await zUpgradePlayerResponse.parseAsync(data);
            },
            url: '/player/upgrade/{player_id}',
            ...options
        });
    }
    
}

export class MatchesService {
    /**
     * Create Match
     * path operation for automatically creating a match, requires a part query.
     */
    public static createMatch<ThrowOnError extends boolean = false>(options: Options<CreateMatchData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<CreateMatchResponse, CreateMatchError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: createMatchResponseTransformer,
            responseValidator: async (data) => {
                return await zCreateMatchResponse.parseAsync(data);
            },
            url: '/match/create',
            ...options
        });
    }
    
    /**
     * Get Matches
     * get all matches
     */
    public static getMatches<ThrowOnError extends boolean = false>(options?: Options<GetMatchesData, ThrowOnError>) {
        return (options?.client ?? _heyApiClient).get<GetMatchesResponse, GetMatchesError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: getMatchesResponseTransformer,
            responseValidator: async (data) => {
                return await zGetMatchesResponse.parseAsync(data);
            },
            url: '/match/all',
            ...options
        });
    }
    
    /**
     * Get Lastest Match
     * get last created match
     */
    public static getLastestMatch<ThrowOnError extends boolean = false>(options?: Options<GetLastestMatchData, ThrowOnError>) {
        return (options?.client ?? _heyApiClient).get<GetLastestMatchResponse, GetLastestMatchError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: getLastestMatchResponseTransformer,
            responseValidator: async (data) => {
                return await zGetLastestMatchResponse.parseAsync(data);
            },
            url: '/match/latest',
            ...options
        });
    }
    
    /**
     * Vote
     * function for casting votes
     *
     * - a match id is required
     * - if an invalid vote cursed application id or player id is submitted, they are ignored.
     */
    public static vote<ThrowOnError extends boolean = false>(options: Options<VoteData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<VoteResponse, VoteError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseValidator: async (data) => {
                return await zVoteResponse.parseAsync(data);
            },
            url: '/match/vote/{match_id}',
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers
            }
        });
    }
    
    /**
     * Domain Expansion
     * Activates the domain of a player in an ongoing match.
     *
     * Buffs the vote to x4 per vote.
     *
     * Weakend by simple domain
     */
    public static domainExpansion<ThrowOnError extends boolean = false>(options: Options<DomainExpansionData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<DomainExpansionResponse, DomainExpansionError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: domainExpansionResponseTransformer,
            responseValidator: async (data) => {
                return await zDomainExpansionResponse.parseAsync(data);
            },
            url: '/match/activate/domain/{player_id}',
            ...options
        });
    }
    
    /**
     * Simple Domain
     * Activates the simple domain of a player in an ongoing match.
     *
     * Which either
     *
     * * Reduces the opponent's vote to half per vote, If opponent doesn't have domain expansion active.
     *
     * or
     * * If opponent's domain is expanded, the simple domain weakens the domain expansion effect
     */
    public static simpleDomain<ThrowOnError extends boolean = false>(options: Options<SimpleDomainData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<SimpleDomainResponse, SimpleDomainError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: simpleDomainResponseTransformer,
            responseValidator: async (data) => {
                return await zSimpleDomainResponse.parseAsync(data);
            },
            url: '/match/activate/simple/{player_id}',
            ...options
        });
    }
    
}

export class AdminService {
    /**
     * Create Admin
     * Creates an admin user with specified permissions.
     */
    public static createAdmin<ThrowOnError extends boolean = false>(options: Options<CreateAdminData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<CreateAdminResponse, CreateAdminError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseTransformer: createAdminResponseTransformer,
            responseValidator: async (data) => {
                return await zCreateAdminResponse.parseAsync(data);
            },
            url: '/admin/create/{user}',
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers
            }
        });
    }
    
    /**
     * New Permission
     * for creating new permissions; only doable by a super user
     */
    public static newPermission<ThrowOnError extends boolean = false>(options: Options<NewPermissionData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<NewPermissionResponse, NewPermissionError, ThrowOnError>({
            security: [
                {
                    scheme: 'bearer',
                    type: 'http'
                }
            ],
            responseValidator: async (data) => {
                return await zNewPermissionResponse.parseAsync(data);
            },
            url: '/admin/new/permission',
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers
            }
        });
    }
    
    /**
     * Demo Superuser
     */
    public static demoSuperuser<ThrowOnError extends boolean = false>(options: Options<DemoSuperuserData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<unknown, DemoSuperuserError, ThrowOnError>({
            url: '/admin/superuser/{user}',
            ...options
        });
    }
    
}

export class AuthService {
    /**
     * creates a login token
     */
    public static createToken<ThrowOnError extends boolean = false>(options: Options<CreateTokenData, ThrowOnError>) {
        return (options.client ?? _heyApiClient).post<CreateTokenResponse, CreateTokenError, ThrowOnError>({
            ...urlSearchParamsBodySerializer,
            responseValidator: async (data) => {
                return await zCreateTokenResponse.parseAsync(data);
            },
            url: '/login',
            ...options,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                ...options?.headers
            }
        });
    }
    
}