// This file is auto-generated by @hey-api/openapi-ts

import { z } from 'zod';

export const zAdminInfo = z.object({
    is_superuser: z.boolean(),
    permissions: z.array(z.object({
        model: z.enum([
            'colony',
            'user',
            'barriertech',
            'barrierrecord',
            'player',
            'cursedtechnique',
            'ctapp',
            'match',
            'vote',
            'adminuser',
            'permission'
        ]),
        name: z.string(),
        level: z.unknown()
    })),
    id: z.number().int(),
    user: z.object({
        username: z.string().regex(/^[A-Za-z][A-Za-z0-9_-]{2,19}$/),
        email: z.string().email(),
        country: z.union([
            z.enum([
                'AF',
                'AL',
                'DZ',
                'AD',
                'AO',
                'AG',
                'AR',
                'AM',
                'AU',
                'AT',
                'AZ',
                'BS',
                'BH',
                'BD',
                'BB',
                'BY',
                'BE',
                'BZ',
                'BJ',
                'BT',
                'BO',
                'BA',
                'BW',
                'BR',
                'BN',
                'BG',
                'BF',
                'BI',
                'CV',
                'KH',
                'CM',
                'CA',
                'CF',
                'TD',
                'CL',
                'CN',
                'CO',
                'KM',
                'CG',
                'CD',
                'CR',
                'HR',
                'CU',
                'CY',
                'CZ',
                'DK',
                'DJ',
                'DM',
                'DO',
                'EC',
                'EG',
                'SV',
                'GQ',
                'ER',
                'EE',
                'SZ',
                'ET',
                'FJ',
                'FI',
                'FR',
                'GA',
                'GM',
                'GE',
                'DE',
                'GH',
                'GR',
                'GD',
                'GT',
                'GN',
                'GW',
                'GY',
                'HT',
                'HN',
                'HU',
                'IS',
                'IN',
                'ID',
                'IR',
                'IQ',
                'IE',
                'IL',
                'IT',
                'JM',
                'JP',
                'JO',
                'KZ',
                'KE',
                'KI',
                'XK',
                'KW',
                'KG',
                'LA',
                'LV',
                'LB',
                'LS',
                'LR',
                'LY',
                'LI',
                'LT',
                'LU',
                'MG',
                'MW',
                'MY',
                'MV',
                'ML',
                'MT',
                'MH',
                'MR',
                'MU',
                'MX',
                'FM',
                'MD',
                'MC',
                'MN',
                'ME',
                'MA',
                'MZ',
                'MM',
                'NA',
                'NR',
                'NP',
                'NL',
                'NZ',
                'NI',
                'NE',
                'NG',
                'KP',
                'MK',
                'NO',
                'OM',
                'PK',
                'PW',
                'PS',
                'PA',
                'PG',
                'PY',
                'PE',
                'PH',
                'PL',
                'PT',
                'QA',
                'RO',
                'RU',
                'RW',
                'KN',
                'LC',
                'VC',
                'WS',
                'SM',
                'ST',
                'SA',
                'SN',
                'RS',
                'SC',
                'SL',
                'SG',
                'SK',
                'SI',
                'SB',
                'SO',
                'ZA',
                'KR',
                'SS',
                'ES',
                'LK',
                'SD',
                'SR',
                'SE',
                'CH',
                'SY',
                'TW',
                'TJ',
                'TZ',
                'TH',
                'TL',
                'TG',
                'TO',
                'TT',
                'TN',
                'TR',
                'TM',
                'TV',
                'UG',
                'UA',
                'AE',
                'GB',
                'US',
                'UY',
                'UZ',
                'VU',
                'VA',
                'VE',
                'VN',
                'YE',
                'ZM',
                'ZW'
            ]),
            z.null()
        ]).optional(),
        id: z.number().int(),
        created: z.string().date()
    })
});

export const zBarrierTechInfo = z.object({
    domain_expansion: z.boolean().optional().default(false),
    binding_vow: z.boolean().optional().default(false),
    simple_domain: z.boolean().optional().default(false),
    de_end_time: z.union([
        z.string().datetime(),
        z.null()
    ]).optional(),
    bv_end_time: z.union([
        z.string().datetime(),
        z.null()
    ]).optional(),
    sd_end_time: z.union([
        z.string().datetime(),
        z.null()
    ]).optional(),
    id: z.number().int()
});

export const zBaseAdminInfo = z.object({
    is_superuser: z.boolean(),
    permissions: z.array(z.object({
        model: z.enum([
            'colony',
            'user',
            'barriertech',
            'barrierrecord',
            'player',
            'cursedtechnique',
            'ctapp',
            'match',
            'vote',
            'adminuser',
            'permission'
        ]),
        name: z.string(),
        level: z.unknown()
    }))
});

export const zBaseCtAppInfo = z.object({
    name: z.string().min(3).max(100),
    application: z.string().min(100).max(500),
    id: z.number().int(),
    number: z.number().int()
});

export const zBaseCtInfo = z.object({
    name: z.string().min(3).max(100),
    definition: z.string().min(50).max(500),
    id: z.number().int(),
    applications: z.array(zBaseCtAppInfo)
});

export const zBaseColonyInfo = z.object({
    country: z.enum([
        'AF',
        'AL',
        'DZ',
        'AD',
        'AO',
        'AG',
        'AR',
        'AM',
        'AU',
        'AT',
        'AZ',
        'BS',
        'BH',
        'BD',
        'BB',
        'BY',
        'BE',
        'BZ',
        'BJ',
        'BT',
        'BO',
        'BA',
        'BW',
        'BR',
        'BN',
        'BG',
        'BF',
        'BI',
        'CV',
        'KH',
        'CM',
        'CA',
        'CF',
        'TD',
        'CL',
        'CN',
        'CO',
        'KM',
        'CG',
        'CD',
        'CR',
        'HR',
        'CU',
        'CY',
        'CZ',
        'DK',
        'DJ',
        'DM',
        'DO',
        'EC',
        'EG',
        'SV',
        'GQ',
        'ER',
        'EE',
        'SZ',
        'ET',
        'FJ',
        'FI',
        'FR',
        'GA',
        'GM',
        'GE',
        'DE',
        'GH',
        'GR',
        'GD',
        'GT',
        'GN',
        'GW',
        'GY',
        'HT',
        'HN',
        'HU',
        'IS',
        'IN',
        'ID',
        'IR',
        'IQ',
        'IE',
        'IL',
        'IT',
        'JM',
        'JP',
        'JO',
        'KZ',
        'KE',
        'KI',
        'XK',
        'KW',
        'KG',
        'LA',
        'LV',
        'LB',
        'LS',
        'LR',
        'LY',
        'LI',
        'LT',
        'LU',
        'MG',
        'MW',
        'MY',
        'MV',
        'ML',
        'MT',
        'MH',
        'MR',
        'MU',
        'MX',
        'FM',
        'MD',
        'MC',
        'MN',
        'ME',
        'MA',
        'MZ',
        'MM',
        'NA',
        'NR',
        'NP',
        'NL',
        'NZ',
        'NI',
        'NE',
        'NG',
        'KP',
        'MK',
        'NO',
        'OM',
        'PK',
        'PW',
        'PS',
        'PA',
        'PG',
        'PY',
        'PE',
        'PH',
        'PL',
        'PT',
        'QA',
        'RO',
        'RU',
        'RW',
        'KN',
        'LC',
        'VC',
        'WS',
        'SM',
        'ST',
        'SA',
        'SN',
        'RS',
        'SC',
        'SL',
        'SG',
        'SK',
        'SI',
        'SB',
        'SO',
        'ZA',
        'KR',
        'SS',
        'ES',
        'LK',
        'SD',
        'SR',
        'SE',
        'CH',
        'SY',
        'TW',
        'TJ',
        'TZ',
        'TH',
        'TL',
        'TG',
        'TO',
        'TT',
        'TN',
        'TR',
        'TM',
        'TV',
        'UG',
        'UA',
        'AE',
        'GB',
        'US',
        'UY',
        'UZ',
        'VU',
        'VA',
        'VE',
        'VN',
        'YE',
        'ZM',
        'ZW'
    ]),
    id: z.number().int()
});

export const zBaseMatchInfo = z.object({
    begin: z.string().datetime(),
    end: z.string().datetime(),
    part: z.number().int(),
    id: z.number().int(),
    winner: z.union([
        z.object({
            name: z.string().min(2).max(50),
            gender: z.enum([
                'male',
                'female',
                'non-binary'
            ]),
            age: z.number().int().gte(10).lte(102),
            role: z.union([
                z.string().min(3).max(50),
                z.null()
            ]).optional(),
            id: z.number().int(),
            created: z.string().date(),
            grade: z.unknown(),
            points: z.number()
        }),
        z.null()
    ])
});

export const zBasePermissionInfo = z.object({
    model: z.enum([
        'colony',
        'user',
        'barriertech',
        'barrierrecord',
        'player',
        'cursedtechnique',
        'ctapp',
        'match',
        'vote',
        'adminuser',
        'permission'
    ]),
    name: z.string(),
    level: z.unknown()
});

export const zBasePlayerInfo = z.object({
    name: z.string().min(2).max(50),
    gender: z.enum([
        'male',
        'female',
        'non-binary'
    ]),
    age: z.number().int().gte(10).lte(102),
    role: z.union([
        z.string().min(3).max(50),
        z.null()
    ]).optional(),
    id: z.number().int(),
    created: z.string().date(),
    grade: z.unknown(),
    points: z.number()
});

export const zBaseUserInfo = z.object({
    username: z.string().regex(/^[A-Za-z][A-Za-z0-9_-]{2,19}$/),
    email: z.string().email(),
    country: z.union([
        z.enum([
            'AF',
            'AL',
            'DZ',
            'AD',
            'AO',
            'AG',
            'AR',
            'AM',
            'AU',
            'AT',
            'AZ',
            'BS',
            'BH',
            'BD',
            'BB',
            'BY',
            'BE',
            'BZ',
            'BJ',
            'BT',
            'BO',
            'BA',
            'BW',
            'BR',
            'BN',
            'BG',
            'BF',
            'BI',
            'CV',
            'KH',
            'CM',
            'CA',
            'CF',
            'TD',
            'CL',
            'CN',
            'CO',
            'KM',
            'CG',
            'CD',
            'CR',
            'HR',
            'CU',
            'CY',
            'CZ',
            'DK',
            'DJ',
            'DM',
            'DO',
            'EC',
            'EG',
            'SV',
            'GQ',
            'ER',
            'EE',
            'SZ',
            'ET',
            'FJ',
            'FI',
            'FR',
            'GA',
            'GM',
            'GE',
            'DE',
            'GH',
            'GR',
            'GD',
            'GT',
            'GN',
            'GW',
            'GY',
            'HT',
            'HN',
            'HU',
            'IS',
            'IN',
            'ID',
            'IR',
            'IQ',
            'IE',
            'IL',
            'IT',
            'JM',
            'JP',
            'JO',
            'KZ',
            'KE',
            'KI',
            'XK',
            'KW',
            'KG',
            'LA',
            'LV',
            'LB',
            'LS',
            'LR',
            'LY',
            'LI',
            'LT',
            'LU',
            'MG',
            'MW',
            'MY',
            'MV',
            'ML',
            'MT',
            'MH',
            'MR',
            'MU',
            'MX',
            'FM',
            'MD',
            'MC',
            'MN',
            'ME',
            'MA',
            'MZ',
            'MM',
            'NA',
            'NR',
            'NP',
            'NL',
            'NZ',
            'NI',
            'NE',
            'NG',
            'KP',
            'MK',
            'NO',
            'OM',
            'PK',
            'PW',
            'PS',
            'PA',
            'PG',
            'PY',
            'PE',
            'PH',
            'PL',
            'PT',
            'QA',
            'RO',
            'RU',
            'RW',
            'KN',
            'LC',
            'VC',
            'WS',
            'SM',
            'ST',
            'SA',
            'SN',
            'RS',
            'SC',
            'SL',
            'SG',
            'SK',
            'SI',
            'SB',
            'SO',
            'ZA',
            'KR',
            'SS',
            'ES',
            'LK',
            'SD',
            'SR',
            'SE',
            'CH',
            'SY',
            'TW',
            'TJ',
            'TZ',
            'TH',
            'TL',
            'TG',
            'TO',
            'TT',
            'TN',
            'TR',
            'TM',
            'TV',
            'UG',
            'UA',
            'AE',
            'GB',
            'US',
            'UY',
            'UZ',
            'VU',
            'VA',
            'VE',
            'VN',
            'YE',
            'ZM',
            'ZW'
        ]),
        z.null()
    ]).optional(),
    id: z.number().int(),
    created: z.string().date()
});

export const zBaseVoteInfo = z.object({
    player_id: z.union([
        z.number().int(),
        z.null()
    ]).optional(),
    ct_app_id: z.union([
        z.number().int(),
        z.null()
    ]).optional(),
    id: z.number().int(),
    user_id: z.number().int(),
    point: z.number(),
    has_been_added: z.boolean().optional().default(false)
});

export const zBodyCreatePlayer = z.object({
    player: z.object({
        name: z.string().min(2).max(50),
        gender: z.enum([
            'male',
            'female',
            'non-binary'
        ]),
        age: z.number().int().gte(10).lte(102),
        role: z.union([
            z.string().min(3).max(50),
            z.null()
        ]).optional()
    }),
    cursed_technique: z.object({
        name: z.string().min(3).max(100),
        definition: z.string().min(50).max(500)
    }),
    applications: z.unknown()
});

export const zBodyCreateToken = z.object({
    grant_type: z.union([
        z.string().regex(/password/),
        z.null()
    ]).optional(),
    username: z.string(),
    password: z.string(),
    scope: z.string().optional().default(''),
    client_id: z.union([
        z.string(),
        z.null()
    ]).optional(),
    client_secret: z.union([
        z.string(),
        z.null()
    ]).optional()
});

export const zBodyEditPlayer = z.object({
    player: z.union([
        z.object({
            name: z.union([
                z.string().min(2).max(50),
                z.null()
            ]).optional(),
            gender: z.union([
                z.enum([
                    'male',
                    'female',
                    'non-binary'
                ]),
                z.null()
            ]).optional(),
            age: z.union([
                z.number().int().gte(10).lte(102),
                z.null()
            ]).optional(),
            role: z.union([
                z.string().min(3).max(50),
                z.null()
            ]).optional()
        }),
        z.null()
    ]).optional(),
    cursed_technique: z.union([
        z.object({
            name: z.union([
                z.string().min(3).max(100),
                z.null()
            ]).optional(),
            definition: z.union([
                z.string().min(50).max(500),
                z.null()
            ]).optional()
        }),
        z.null()
    ]).optional(),
    applications: z.union([
        z.array(z.object({
            number: z.number().int().gte(1).lte(5),
            name: z.union([
                z.string().min(3).max(100),
                z.null()
            ]).optional(),
            application: z.union([
                z.string().min(100).max(500),
                z.null()
            ]).optional()
        })).max(5),
        z.null()
    ]).optional()
});

export const zCastVote = z.object({
    player_id: z.number().int(),
    ct_app_id: z.number().int()
});

export const zClientVoteInfo = z.object({
    message: z.string(),
    votes: z.array(zBaseVoteInfo)
});

export const zColonyInfo = z.object({
    country: z.enum([
        'AF',
        'AL',
        'DZ',
        'AD',
        'AO',
        'AG',
        'AR',
        'AM',
        'AU',
        'AT',
        'AZ',
        'BS',
        'BH',
        'BD',
        'BB',
        'BY',
        'BE',
        'BZ',
        'BJ',
        'BT',
        'BO',
        'BA',
        'BW',
        'BR',
        'BN',
        'BG',
        'BF',
        'BI',
        'CV',
        'KH',
        'CM',
        'CA',
        'CF',
        'TD',
        'CL',
        'CN',
        'CO',
        'KM',
        'CG',
        'CD',
        'CR',
        'HR',
        'CU',
        'CY',
        'CZ',
        'DK',
        'DJ',
        'DM',
        'DO',
        'EC',
        'EG',
        'SV',
        'GQ',
        'ER',
        'EE',
        'SZ',
        'ET',
        'FJ',
        'FI',
        'FR',
        'GA',
        'GM',
        'GE',
        'DE',
        'GH',
        'GR',
        'GD',
        'GT',
        'GN',
        'GW',
        'GY',
        'HT',
        'HN',
        'HU',
        'IS',
        'IN',
        'ID',
        'IR',
        'IQ',
        'IE',
        'IL',
        'IT',
        'JM',
        'JP',
        'JO',
        'KZ',
        'KE',
        'KI',
        'XK',
        'KW',
        'KG',
        'LA',
        'LV',
        'LB',
        'LS',
        'LR',
        'LY',
        'LI',
        'LT',
        'LU',
        'MG',
        'MW',
        'MY',
        'MV',
        'ML',
        'MT',
        'MH',
        'MR',
        'MU',
        'MX',
        'FM',
        'MD',
        'MC',
        'MN',
        'ME',
        'MA',
        'MZ',
        'MM',
        'NA',
        'NR',
        'NP',
        'NL',
        'NZ',
        'NI',
        'NE',
        'NG',
        'KP',
        'MK',
        'NO',
        'OM',
        'PK',
        'PW',
        'PS',
        'PA',
        'PG',
        'PY',
        'PE',
        'PH',
        'PL',
        'PT',
        'QA',
        'RO',
        'RU',
        'RW',
        'KN',
        'LC',
        'VC',
        'WS',
        'SM',
        'ST',
        'SA',
        'SN',
        'RS',
        'SC',
        'SL',
        'SG',
        'SK',
        'SI',
        'SB',
        'SO',
        'ZA',
        'KR',
        'SS',
        'ES',
        'LK',
        'SD',
        'SR',
        'SE',
        'CH',
        'SY',
        'TW',
        'TJ',
        'TZ',
        'TH',
        'TL',
        'TG',
        'TO',
        'TT',
        'TN',
        'TR',
        'TM',
        'TV',
        'UG',
        'UA',
        'AE',
        'GB',
        'US',
        'UY',
        'UZ',
        'VU',
        'VA',
        'VE',
        'VN',
        'YE',
        'ZM',
        'ZW'
    ]),
    id: z.number().int(),
    players: z.array(zBasePlayerInfo)
});

export const zCountry = z.enum([
    'AF',
    'AL',
    'DZ',
    'AD',
    'AO',
    'AG',
    'AR',
    'AM',
    'AU',
    'AT',
    'AZ',
    'BS',
    'BH',
    'BD',
    'BB',
    'BY',
    'BE',
    'BZ',
    'BJ',
    'BT',
    'BO',
    'BA',
    'BW',
    'BR',
    'BN',
    'BG',
    'BF',
    'BI',
    'CV',
    'KH',
    'CM',
    'CA',
    'CF',
    'TD',
    'CL',
    'CN',
    'CO',
    'KM',
    'CG',
    'CD',
    'CR',
    'HR',
    'CU',
    'CY',
    'CZ',
    'DK',
    'DJ',
    'DM',
    'DO',
    'EC',
    'EG',
    'SV',
    'GQ',
    'ER',
    'EE',
    'SZ',
    'ET',
    'FJ',
    'FI',
    'FR',
    'GA',
    'GM',
    'GE',
    'DE',
    'GH',
    'GR',
    'GD',
    'GT',
    'GN',
    'GW',
    'GY',
    'HT',
    'HN',
    'HU',
    'IS',
    'IN',
    'ID',
    'IR',
    'IQ',
    'IE',
    'IL',
    'IT',
    'JM',
    'JP',
    'JO',
    'KZ',
    'KE',
    'KI',
    'XK',
    'KW',
    'KG',
    'LA',
    'LV',
    'LB',
    'LS',
    'LR',
    'LY',
    'LI',
    'LT',
    'LU',
    'MG',
    'MW',
    'MY',
    'MV',
    'ML',
    'MT',
    'MH',
    'MR',
    'MU',
    'MX',
    'FM',
    'MD',
    'MC',
    'MN',
    'ME',
    'MA',
    'MZ',
    'MM',
    'NA',
    'NR',
    'NP',
    'NL',
    'NZ',
    'NI',
    'NE',
    'NG',
    'KP',
    'MK',
    'NO',
    'OM',
    'PK',
    'PW',
    'PS',
    'PA',
    'PG',
    'PY',
    'PE',
    'PH',
    'PL',
    'PT',
    'QA',
    'RO',
    'RU',
    'RW',
    'KN',
    'LC',
    'VC',
    'WS',
    'SM',
    'ST',
    'SA',
    'SN',
    'RS',
    'SC',
    'SL',
    'SG',
    'SK',
    'SI',
    'SB',
    'SO',
    'ZA',
    'KR',
    'SS',
    'ES',
    'LK',
    'SD',
    'SR',
    'SE',
    'CH',
    'SY',
    'TW',
    'TJ',
    'TZ',
    'TH',
    'TL',
    'TG',
    'TO',
    'TT',
    'TN',
    'TR',
    'TM',
    'TV',
    'UG',
    'UA',
    'AE',
    'GB',
    'US',
    'UY',
    'UZ',
    'VU',
    'VA',
    'VE',
    'VN',
    'YE',
    'ZM',
    'ZW'
]);

export const zCreateCt = z.object({
    name: z.string().min(3).max(100),
    definition: z.string().min(50).max(500)
});

export const zCreateCtApp = z.object({
    name: z.string().min(3).max(100),
    application: z.string().min(100).max(500)
});

export const zCreatePermission = z.object({
    model: z.enum([
        'colony',
        'user',
        'barriertech',
        'barrierrecord',
        'player',
        'cursedtechnique',
        'ctapp',
        'match',
        'vote',
        'adminuser',
        'permission'
    ]),
    level: z.array(z.unknown())
});

export const zCreatePlayer = z.object({
    name: z.string().min(2).max(50),
    gender: z.enum([
        'male',
        'female',
        'non-binary'
    ]),
    age: z.number().int().gte(10).lte(102),
    role: z.union([
        z.string().min(3).max(50),
        z.null()
    ]).optional()
});

export const zCreateUser = z.object({
    username: z.string().regex(/^[A-Za-z][A-Za-z0-9_-]{2,19}$/),
    email: z.string().email(),
    country: z.union([
        zCountry,
        z.null()
    ]).optional(),
    password: z.string(),
    confirm_password: z.string()
});

export const zEditCt = z.object({
    name: z.union([
        z.string().min(3).max(100),
        z.null()
    ]).optional(),
    definition: z.union([
        z.string().min(50).max(500),
        z.null()
    ]).optional()
});

export const zEditCtApp = z.object({
    number: z.number().int().gte(1).lte(5),
    name: z.union([
        z.string().min(3).max(100),
        z.null()
    ]).optional(),
    application: z.union([
        z.string().min(100).max(500),
        z.null()
    ]).optional()
});

export const zEditPlayer = z.object({
    name: z.union([
        z.string().min(2).max(50),
        z.null()
    ]).optional(),
    gender: z.union([
        z.enum([
            'male',
            'female',
            'non-binary'
        ]),
        z.null()
    ]).optional(),
    age: z.union([
        z.number().int().gte(10).lte(102),
        z.null()
    ]).optional(),
    role: z.union([
        z.string().min(3).max(50),
        z.null()
    ]).optional()
});

export const zEditUser = z.object({
    username: z.union([
        z.string().regex(/^[A-Za-z][A-Za-z0-9_-]{2,19}$/),
        z.null()
    ]).optional(),
    email: z.union([
        z.string().email(),
        z.null()
    ]).optional(),
    country: z.union([
        zCountry,
        z.null()
    ]).optional()
});

export const zGender = z.enum([
    'male',
    'female',
    'non-binary'
]);

export const zGrade = z.unknown();

export const zHttpValidationError = z.object({
    detail: z.array(z.object({
        loc: z.array(z.unknown()),
        msg: z.string(),
        type: z.string()
    })).optional()
});

export const zMatchInfo = z.object({
    begin: z.coerce.string().datetime(),
    end: z.coerce.string().datetime(),
    part: z.number().int(),
    id: z.number().int(),
    winner: z.union([
        zBasePlayerInfo,
        z.null()
    ]),
    players: z.array(zBasePlayerInfo),
    colony: zBaseColonyInfo
});

export const zModelName = z.enum([
    'colony',
    'user',
    'barriertech',
    'barrierrecord',
    'player',
    'cursedtechnique',
    'ctapp',
    'match',
    'vote',
    'adminuser',
    'permission'
]);

export const zPermissionInfo = z.object({
    model: zModelName,
    name: z.string(),
    level: z.unknown(),
    id: z.number().int()
});

export const zPermissionLevel = z.unknown();

export const zPlayerInfo = z.object({
    name: z.string().min(2).max(50),
    gender: zGender,
    age: z.number().int().gte(10).lte(102),
    role: z.union([
        z.string().min(3).max(50),
        z.null()
    ]).optional(),
    id: z.number().int(),
    created: z.string().date(),
    grade: zGrade,
    points: z.number(),
    cursed_technique: zBaseCtInfo,
    barrier_technique: z.union([
        zBarrierTechInfo,
        z.null()
    ]),
    colony: z.union([
        zBaseColonyInfo,
        z.null()
    ]),
    user: z.union([
        zBaseUserInfo,
        z.null()
    ]),
    matches: z.array(zBaseMatchInfo)
});

export const zToken = z.object({
    access_token: z.string(),
    token_type: z.string()
});

export const zUserInfo = z.object({
    username: z.string().regex(/^[A-Za-z][A-Za-z0-9_-]{2,19}$/),
    email: z.string().email(),
    country: z.union([
        zCountry,
        z.null()
    ]).optional(),
    id: z.number().int(),
    created: z.string().date(),
    player: z.union([
        zBasePlayerInfo,
        z.null()
    ]).optional(),
    admin: z.union([
        zBaseAdminInfo,
        z.null()
    ]).optional()
});

export const zValidationError = z.object({
    loc: z.array(z.unknown()),
    msg: z.string(),
    type: z.string()
});

export const zCurrentUserResponse = zUserInfo;

export const zAUserResponse = zUserInfo;

export const zEditUserResponse = zUserInfo;

export const zDeleteUserResponse = zUserInfo;

export const zCreatePlayerResponse = zPlayerInfo;

export const zMyPlayerResponse = zPlayerInfo;

export const zGetPlayersResponse = z.union([
    z.array(zPlayerInfo),
    z.array(zBasePlayerInfo)
]);

export const zAPlayerResponse = zPlayerInfo;

export const zEditPlayerResponse = zPlayerInfo;

export const zDeletePlayerResponse = zPlayerInfo;

export const zUpgradePlayerResponse = zPlayerInfo;

export const zCreateMatchResponse = zMatchInfo;

export const zGetMatchesResponse = z.array(zMatchInfo);

export const zGetLastestMatchResponse = zMatchInfo;

export const zVoteResponse = zClientVoteInfo;

export const zDomainExpansionResponse = zBarrierTechInfo;

export const zSimpleDomainResponse = zBarrierTechInfo;

export const zCreateAdminResponse = zAdminInfo;

export const zNewPermissionResponse = z.array(zPermissionInfo);

export const zGetColoniesResponse = z.array(zColonyInfo);

export const zCreateTokenResponse = zToken;

export const zCreateUserResponse = zUserInfo;