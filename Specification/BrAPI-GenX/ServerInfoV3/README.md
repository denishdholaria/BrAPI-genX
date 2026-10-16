# BrAPI GenX — ServerInfoV3

Capability negotiation for GenX servers, served under `/brapi/v3/`.

`GET /brapi/v3/serverinfo` (`genxGetServerInfoV3`) returns `ServerInfoV3`
(`Schemas/ServerInfoV3.yaml`): every V2.1 `ServerInfo` field plus
`brapiVersions[]`, `capabilities[]{name, versions, methods, scopes}`, and
`authProfiles[]{name, issuer, scopes}`.

Clients negotiate from this document instead of probing endpoints. A GenX
client against a V2.1-only server falls back to the V2.1 `serverinfo` `calls`
array. V2.1 `GET /brapi/v2/serverinfo` is unchanged.
