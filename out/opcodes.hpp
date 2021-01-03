#pragma once
namespace kumo
{
    enum class opcode
    {
        handshake        = 0x047b,
        handshake_response = 0x7a01,
        login            = 0x40ea,
        login_response   = 0x54f0,
        characters_list  = 0x4b05,
        character_selected = 0x2e6b,
        enter_world      = 0x5f9f,
        do_sth           = 0x71bb,
        spawn            = 0x3858,
        move             = 0x15af,
        player_information = 0x053f,
        spawned_entity   = 0x392b,
        despawned_entity = 0x1393,
        world_update     = 0x5d15,
    };
}
