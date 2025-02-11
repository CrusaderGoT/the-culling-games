// This file is auto-generated by @hey-api/openapi-ts

import type { CurrentUserResponse, AuserResponse, EditUserResponse, DeleteUserResponse, CreatePlayerResponse, MyPlayerResponse, APlayerResponse, EditPlayerResponse, DeletePlayerResponse, UpgradePlayerResponse, CreateMatchResponse, GetMatchesResponse, GetLastestMatchResponse, DomainExpansionResponse, SimpleDomainResponse, CreateAdminResponse, CreateUserResponse } from './types.gen';

const basePlayerInfoSchemaResponseTransformer = (data: any) => {
    data.created = new Date(data.created);
    return data;
};

const userInfoSchemaResponseTransformer = (data: any) => {
    data.created = new Date(data.created);
    if (data.player) {
        data.player = basePlayerInfoSchemaResponseTransformer(data.player);
    }
    return data;
};

export const currentUserResponseTransformer = async (data: any): Promise<CurrentUserResponse> => {
    data = userInfoSchemaResponseTransformer(data);
    return data;
};

export const aUserResponseTransformer = async (data: any): Promise<AuserResponse> => {
    data = userInfoSchemaResponseTransformer(data);
    return data;
};

export const editUserResponseTransformer = async (data: any): Promise<EditUserResponse> => {
    data = userInfoSchemaResponseTransformer(data);
    return data;
};

export const deleteUserResponseTransformer = async (data: any): Promise<DeleteUserResponse> => {
    data = userInfoSchemaResponseTransformer(data);
    return data;
};

const barrierTechInfoSchemaResponseTransformer = (data: any) => {
    if (data.de_end_time) {
        data.de_end_time = new Date(data.de_end_time);
    }
    if (data.bv_end_time) {
        data.bv_end_time = new Date(data.bv_end_time);
    }
    if (data.sd_end_time) {
        data.sd_end_time = new Date(data.sd_end_time);
    }
    return data;
};

const baseUserInfoSchemaResponseTransformer = (data: any) => {
    data.created = new Date(data.created);
    return data;
};

const baseMatchInfoSchemaResponseTransformer = (data: any) => {
    data.begin = new Date(data.begin);
    data.end = new Date(data.end);
    data.winner = basePlayerInfoSchemaResponseTransformer(data.winner);
    return data;
};

const playerInfoSchemaResponseTransformer = (data: any) => {
    data.created = new Date(data.created);
    data.barrier_technique = barrierTechInfoSchemaResponseTransformer(data.barrier_technique);
    data.user = baseUserInfoSchemaResponseTransformer(data.user);
    data.matches = data.matches.map((item: any) => {
        return baseMatchInfoSchemaResponseTransformer(item);
    });
    return data;
};

export const createPlayerResponseTransformer = async (data: any): Promise<CreatePlayerResponse> => {
    data = playerInfoSchemaResponseTransformer(data);
    return data;
};

export const myPlayerResponseTransformer = async (data: any): Promise<MyPlayerResponse> => {
    data = playerInfoSchemaResponseTransformer(data);
    return data;
};

export const aPlayerResponseTransformer = async (data: any): Promise<APlayerResponse> => {
    data = playerInfoSchemaResponseTransformer(data);
    return data;
};

export const editPlayerResponseTransformer = async (data: any): Promise<EditPlayerResponse> => {
    data = playerInfoSchemaResponseTransformer(data);
    return data;
};

export const deletePlayerResponseTransformer = async (data: any): Promise<DeletePlayerResponse> => {
    data = playerInfoSchemaResponseTransformer(data);
    return data;
};

export const upgradePlayerResponseTransformer = async (data: any): Promise<UpgradePlayerResponse> => {
    data = playerInfoSchemaResponseTransformer(data);
    return data;
};

const matchInfoSchemaResponseTransformer = (data: any) => {
    data.begin = new Date(data.begin);
    data.end = new Date(data.end);
    data.winner = basePlayerInfoSchemaResponseTransformer(data.winner);
    data.players = data.players.map((item: any) => {
        return basePlayerInfoSchemaResponseTransformer(item);
    });
    return data;
};

export const createMatchResponseTransformer = async (data: any): Promise<CreateMatchResponse> => {
    data = matchInfoSchemaResponseTransformer(data);
    return data;
};

export const getMatchesResponseTransformer = async (data: any): Promise<GetMatchesResponse> => {
    data = data.map((item: any) => {
        return matchInfoSchemaResponseTransformer(item);
    });
    return data;
};

export const getLastestMatchResponseTransformer = async (data: any): Promise<GetLastestMatchResponse> => {
    data = matchInfoSchemaResponseTransformer(data);
    return data;
};

export const domainExpansionResponseTransformer = async (data: any): Promise<DomainExpansionResponse> => {
    data = barrierTechInfoSchemaResponseTransformer(data);
    return data;
};

export const simpleDomainResponseTransformer = async (data: any): Promise<SimpleDomainResponse> => {
    data = barrierTechInfoSchemaResponseTransformer(data);
    return data;
};

const adminInfoSchemaResponseTransformer = (data: any) => {
    data.user = baseUserInfoSchemaResponseTransformer(data.user);
    return data;
};

export const createAdminResponseTransformer = async (data: any): Promise<CreateAdminResponse> => {
    data = adminInfoSchemaResponseTransformer(data);
    return data;
};

export const createUserResponseTransformer = async (data: any): Promise<CreateUserResponse> => {
    data = userInfoSchemaResponseTransformer(data);
    return data;
};