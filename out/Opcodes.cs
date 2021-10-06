namespace Kumo
{
    public enum Opcodes
    {
        opcodeCreateCharacter    = 0x4913,
        opcodeCharacterCreated   = 0x0a32,
        opcodeClientUpdate       = 0x31a0,
        opcodeHandshake          = 0x047b,
        opcodeHandshakeResponse  = 0x7a01,
        opcodeLogin              = 0x40ea,
        opcodeLoginResponse      = 0x54f0,
        opcodeCharactersList     = 0x4b05,
        opcodeCharacterInformation = 0x0743,
        opcodeLoginCharacter     = 0x4702,
        opcodeLoginCharacterResult = 0x0fe7,
        opcodeEnterWorld         = 0x5f9f,
        opcodeDoSth              = 0x71bb,
        opcodeSpawn              = 0x3858,
        opcodeMove               = 0x15af,
        opcodeSelectedCharacterSpawnData = 0x3ead,
        opcodeSpawnedEntity      = 0x392b,
        opcodeDespawnedEntity    = 0x1393,
        opcodeWorldUpdate        = 0x5d15,
        opcodeSelfWorldUpdate    = 0x1e5c,
    }
}
