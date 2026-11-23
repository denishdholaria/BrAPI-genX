# Group ServerInfoV3

Capability negotiation for GenX servers under /genx/v1/. Returns ServerInfoV3 with all V2.1 ServerInfo fields plus brapiVersions, capabilities, and authProfiles. Clients negotiate from this document instead of probing endpoints; V2.1-only servers fall back to the V2.1 serverinfo calls array.
