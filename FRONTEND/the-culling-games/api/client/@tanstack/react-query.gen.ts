// This file is auto-generated by @hey-api/openapi-ts

import { type Options, UsersService, PlayersService, MatchesService, AdminService, ColoniesService, AuthService } from '../sdk.gen';
import { queryOptions, type UseMutationOptions, infiniteQueryOptions, type InfiniteData } from '@tanstack/react-query';
import type { CurrentUserData, AuserData, EditUserData, EditUserError, EditUserResponse, DeleteUserData, DeleteUserError, DeleteUserResponse, CreatePlayerData, CreatePlayerError, CreatePlayerResponse, MyPlayerData, GetPlayersData, GetPlayersError, GetPlayersResponse, APlayerData, EditPlayerData, EditPlayerError, EditPlayerResponse, DeletePlayerData, DeletePlayerError, DeletePlayerResponse, UpgradePlayerData, UpgradePlayerError, UpgradePlayerResponse, CreateMatchData, CreateMatchError, CreateMatchResponse, GetMatchesData, GetMatchesError, GetMatchesResponse, GetLastestMatchData, VoteData, VoteError, VoteResponse, DomainExpansionData, DomainExpansionError, DomainExpansionResponse, SimpleDomainData, SimpleDomainError, SimpleDomainResponse, CreateAdminData, CreateAdminError, CreateAdminResponse, NewPermissionData, NewPermissionError, NewPermissionResponse, DemoSuperuserData, DemoSuperuserError, GetColoniesData, GetColoniesError, GetColoniesResponse, CreateTokenData, CreateTokenError, CreateTokenResponse, CreateUserData, CreateUserError, CreateUserResponse } from '../types.gen';
import { client as _heyApiClient } from '../client.gen';

export type QueryKey<TOptions extends Options> = [
    Pick<TOptions, 'baseUrl' | 'body' | 'headers' | 'path' | 'query'> & {
        _id: string;
        _infinite?: boolean;
    }
];

const createQueryKey = <TOptions extends Options>(id: string, options?: TOptions, infinite?: boolean): [
    QueryKey<TOptions>[0]
] => {
    const params: QueryKey<TOptions>[0] = { _id: id, baseUrl: (options?.client ?? _heyApiClient).getConfig().baseUrl } as QueryKey<TOptions>[0];
    if (infinite) {
        params._infinite = infinite;
    }
    if (options?.body) {
        params.body = options.body;
    }
    if (options?.headers) {
        params.headers = options.headers;
    }
    if (options?.path) {
        params.path = options.path;
    }
    if (options?.query) {
        params.query = options.query;
    }
    return [
        params
    ];
};

export const currentUserQueryKey = (options?: Options<CurrentUserData>) => createQueryKey('currentUser', options);

export const currentUserOptions = (options?: Options<CurrentUserData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await UsersService.currentUser({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: currentUserQueryKey(options)
    });
};

export const aUserQueryKey = (options: Options<AuserData>) => createQueryKey('aUser', options);

export const aUserOptions = (options: Options<AuserData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await UsersService.aUser({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: aUserQueryKey(options)
    });
};

export const editUserMutation = (options?: Partial<Options<EditUserData>>) => {
    const mutationOptions: UseMutationOptions<EditUserResponse, EditUserError, Options<EditUserData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await UsersService.editUser({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const deleteUserMutation = (options?: Partial<Options<DeleteUserData>>) => {
    const mutationOptions: UseMutationOptions<DeleteUserResponse, DeleteUserError, Options<DeleteUserData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await UsersService.deleteUser({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const createPlayerQueryKey = (options: Options<CreatePlayerData>) => createQueryKey('createPlayer', options);

export const createPlayerOptions = (options: Options<CreatePlayerData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await PlayersService.createPlayer({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: createPlayerQueryKey(options)
    });
};

export const createPlayerMutation = (options?: Partial<Options<CreatePlayerData>>) => {
    const mutationOptions: UseMutationOptions<CreatePlayerResponse, CreatePlayerError, Options<CreatePlayerData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await PlayersService.createPlayer({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const myPlayerQueryKey = (options?: Options<MyPlayerData>) => createQueryKey('myPlayer', options);

export const myPlayerOptions = (options?: Options<MyPlayerData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await PlayersService.myPlayer({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: myPlayerQueryKey(options)
    });
};

export const getPlayersQueryKey = (options?: Options<GetPlayersData>) => createQueryKey('getPlayers', options);

export const getPlayersOptions = (options?: Options<GetPlayersData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await PlayersService.getPlayers({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: getPlayersQueryKey(options)
    });
};

const createInfiniteParams = <K extends Pick<QueryKey<Options>[0], 'body' | 'headers' | 'path' | 'query'>>(queryKey: QueryKey<Options>, page: K) => {
    const params = queryKey[0];
    if (page.body) {
        params.body = {
            ...queryKey[0].body as any,
            ...page.body as any
        };
    }
    if (page.headers) {
        params.headers = {
            ...queryKey[0].headers,
            ...page.headers
        };
    }
    if (page.path) {
        params.path = {
            ...queryKey[0].path as any,
            ...page.path as any
        };
    }
    if (page.query) {
        params.query = {
            ...queryKey[0].query as any,
            ...page.query as any
        };
    }
    return params as unknown as typeof page;
};

export const getPlayersInfiniteQueryKey = (options?: Options<GetPlayersData>): QueryKey<Options<GetPlayersData>> => createQueryKey('getPlayers', options, true);

export const getPlayersInfiniteOptions = (options?: Options<GetPlayersData>) => {
    return infiniteQueryOptions<GetPlayersResponse, GetPlayersError, InfiniteData<GetPlayersResponse>, QueryKey<Options<GetPlayersData>>, number | Pick<QueryKey<Options<GetPlayersData>>[0], 'body' | 'headers' | 'path' | 'query'>>(
    // @ts-ignore
    {
        queryFn: async ({ pageParam, queryKey, signal }) => {
            // @ts-ignore
            const page: Pick<QueryKey<Options<GetPlayersData>>[0], 'body' | 'headers' | 'path' | 'query'> = typeof pageParam === 'object' ? pageParam : {
                query: {
                    offset: pageParam
                }
            };
            const params = createInfiniteParams(queryKey, page);
            const { data } = await PlayersService.getPlayers({
                ...options,
                ...params,
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: getPlayersInfiniteQueryKey(options)
    });
};

export const aPlayerQueryKey = (options: Options<APlayerData>) => createQueryKey('aPlayer', options);

export const aPlayerOptions = (options: Options<APlayerData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await PlayersService.aPlayer({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: aPlayerQueryKey(options)
    });
};

export const editPlayerMutation = (options?: Partial<Options<EditPlayerData>>) => {
    const mutationOptions: UseMutationOptions<EditPlayerResponse, EditPlayerError, Options<EditPlayerData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await PlayersService.editPlayer({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const deletePlayerMutation = (options?: Partial<Options<DeletePlayerData>>) => {
    const mutationOptions: UseMutationOptions<DeletePlayerResponse, DeletePlayerError, Options<DeletePlayerData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await PlayersService.deletePlayer({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const upgradePlayerQueryKey = (options: Options<UpgradePlayerData>) => createQueryKey('upgradePlayer', options);

export const upgradePlayerOptions = (options: Options<UpgradePlayerData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await PlayersService.upgradePlayer({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: upgradePlayerQueryKey(options)
    });
};

export const upgradePlayerMutation = (options?: Partial<Options<UpgradePlayerData>>) => {
    const mutationOptions: UseMutationOptions<UpgradePlayerResponse, UpgradePlayerError, Options<UpgradePlayerData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await PlayersService.upgradePlayer({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const createMatchQueryKey = (options: Options<CreateMatchData>) => createQueryKey('createMatch', options);

export const createMatchOptions = (options: Options<CreateMatchData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await MatchesService.createMatch({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: createMatchQueryKey(options)
    });
};

export const createMatchMutation = (options?: Partial<Options<CreateMatchData>>) => {
    const mutationOptions: UseMutationOptions<CreateMatchResponse, CreateMatchError, Options<CreateMatchData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await MatchesService.createMatch({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const getMatchesQueryKey = (options?: Options<GetMatchesData>) => createQueryKey('getMatches', options);

export const getMatchesOptions = (options?: Options<GetMatchesData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await MatchesService.getMatches({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: getMatchesQueryKey(options)
    });
};

export const getMatchesInfiniteQueryKey = (options?: Options<GetMatchesData>): QueryKey<Options<GetMatchesData>> => createQueryKey('getMatches', options, true);

export const getMatchesInfiniteOptions = (options?: Options<GetMatchesData>) => {
    return infiniteQueryOptions<GetMatchesResponse, GetMatchesError, InfiniteData<GetMatchesResponse>, QueryKey<Options<GetMatchesData>>, number | Pick<QueryKey<Options<GetMatchesData>>[0], 'body' | 'headers' | 'path' | 'query'>>(
    // @ts-ignore
    {
        queryFn: async ({ pageParam, queryKey, signal }) => {
            // @ts-ignore
            const page: Pick<QueryKey<Options<GetMatchesData>>[0], 'body' | 'headers' | 'path' | 'query'> = typeof pageParam === 'object' ? pageParam : {
                query: {
                    offset: pageParam
                }
            };
            const params = createInfiniteParams(queryKey, page);
            const { data } = await MatchesService.getMatches({
                ...options,
                ...params,
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: getMatchesInfiniteQueryKey(options)
    });
};

export const getLastestMatchQueryKey = (options?: Options<GetLastestMatchData>) => createQueryKey('getLastestMatch', options);

export const getLastestMatchOptions = (options?: Options<GetLastestMatchData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await MatchesService.getLastestMatch({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: getLastestMatchQueryKey(options)
    });
};

export const voteQueryKey = (options: Options<VoteData>) => createQueryKey('vote', options);

export const voteOptions = (options: Options<VoteData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await MatchesService.vote({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: voteQueryKey(options)
    });
};

export const voteMutation = (options?: Partial<Options<VoteData>>) => {
    const mutationOptions: UseMutationOptions<VoteResponse, VoteError, Options<VoteData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await MatchesService.vote({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const domainExpansionQueryKey = (options: Options<DomainExpansionData>) => createQueryKey('domainExpansion', options);

export const domainExpansionOptions = (options: Options<DomainExpansionData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await MatchesService.domainExpansion({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: domainExpansionQueryKey(options)
    });
};

export const domainExpansionMutation = (options?: Partial<Options<DomainExpansionData>>) => {
    const mutationOptions: UseMutationOptions<DomainExpansionResponse, DomainExpansionError, Options<DomainExpansionData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await MatchesService.domainExpansion({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const simpleDomainQueryKey = (options: Options<SimpleDomainData>) => createQueryKey('simpleDomain', options);

export const simpleDomainOptions = (options: Options<SimpleDomainData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await MatchesService.simpleDomain({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: simpleDomainQueryKey(options)
    });
};

export const simpleDomainMutation = (options?: Partial<Options<SimpleDomainData>>) => {
    const mutationOptions: UseMutationOptions<SimpleDomainResponse, SimpleDomainError, Options<SimpleDomainData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await MatchesService.simpleDomain({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const createAdminQueryKey = (options: Options<CreateAdminData>) => createQueryKey('createAdmin', options);

export const createAdminOptions = (options: Options<CreateAdminData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await AdminService.createAdmin({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: createAdminQueryKey(options)
    });
};

export const createAdminMutation = (options?: Partial<Options<CreateAdminData>>) => {
    const mutationOptions: UseMutationOptions<CreateAdminResponse, CreateAdminError, Options<CreateAdminData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await AdminService.createAdmin({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const newPermissionQueryKey = (options: Options<NewPermissionData>) => createQueryKey('newPermission', options);

export const newPermissionOptions = (options: Options<NewPermissionData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await AdminService.newPermission({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: newPermissionQueryKey(options)
    });
};

export const newPermissionMutation = (options?: Partial<Options<NewPermissionData>>) => {
    const mutationOptions: UseMutationOptions<NewPermissionResponse, NewPermissionError, Options<NewPermissionData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await AdminService.newPermission({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const demoSuperuserQueryKey = (options: Options<DemoSuperuserData>) => createQueryKey('demoSuperuser', options);

export const demoSuperuserOptions = (options: Options<DemoSuperuserData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await AdminService.demoSuperuser({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: demoSuperuserQueryKey(options)
    });
};

export const demoSuperuserMutation = (options?: Partial<Options<DemoSuperuserData>>) => {
    const mutationOptions: UseMutationOptions<unknown, DemoSuperuserError, Options<DemoSuperuserData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await AdminService.demoSuperuser({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const getColoniesQueryKey = (options?: Options<GetColoniesData>) => createQueryKey('getColonies', options);

export const getColoniesOptions = (options?: Options<GetColoniesData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await ColoniesService.getColonies({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: getColoniesQueryKey(options)
    });
};

export const getColoniesInfiniteQueryKey = (options?: Options<GetColoniesData>): QueryKey<Options<GetColoniesData>> => createQueryKey('getColonies', options, true);

export const getColoniesInfiniteOptions = (options?: Options<GetColoniesData>) => {
    return infiniteQueryOptions<GetColoniesResponse, GetColoniesError, InfiniteData<GetColoniesResponse>, QueryKey<Options<GetColoniesData>>, number | Pick<QueryKey<Options<GetColoniesData>>[0], 'body' | 'headers' | 'path' | 'query'>>(
    // @ts-ignore
    {
        queryFn: async ({ pageParam, queryKey, signal }) => {
            // @ts-ignore
            const page: Pick<QueryKey<Options<GetColoniesData>>[0], 'body' | 'headers' | 'path' | 'query'> = typeof pageParam === 'object' ? pageParam : {
                query: {
                    offset: pageParam
                }
            };
            const params = createInfiniteParams(queryKey, page);
            const { data } = await ColoniesService.getColonies({
                ...options,
                ...params,
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: getColoniesInfiniteQueryKey(options)
    });
};

export const createTokenQueryKey = (options: Options<CreateTokenData>) => createQueryKey('createToken', options);

export const createTokenOptions = (options: Options<CreateTokenData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await AuthService.createToken({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: createTokenQueryKey(options)
    });
};

export const createTokenMutation = (options?: Partial<Options<CreateTokenData>>) => {
    const mutationOptions: UseMutationOptions<CreateTokenResponse, CreateTokenError, Options<CreateTokenData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await AuthService.createToken({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};

export const createUserQueryKey = (options: Options<CreateUserData>) => createQueryKey('createUser', options);

export const createUserOptions = (options: Options<CreateUserData>) => {
    return queryOptions({
        queryFn: async ({ queryKey, signal }) => {
            const { data } = await UsersService.createUser({
                ...options,
                ...queryKey[0],
                signal,
                throwOnError: true
            });
            return data;
        },
        queryKey: createUserQueryKey(options)
    });
};

export const createUserMutation = (options?: Partial<Options<CreateUserData>>) => {
    const mutationOptions: UseMutationOptions<CreateUserResponse, CreateUserError, Options<CreateUserData>> = {
        mutationFn: async (localOptions) => {
            const { data } = await UsersService.createUser({
                ...options,
                ...localOptions,
                throwOnError: true
            });
            return data;
        }
    };
    return mutationOptions;
};