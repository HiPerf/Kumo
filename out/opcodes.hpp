#pragma once
namespace kumo
{
    enum class opcode
    {
        create_character = 0x4913,
        character_created = 0x0a32,
        client_update    = 0x31a0,
        handshake        = 0x047b,
        handshake_response = 0x7a01,
        login            = 0x40ea,
        login_response   = 0x54f0,
        characters_list  = 0x4b05,
        character_information = 0x0743,
        login_character  = 0x4702,
        login_character_result = 0x0fe7,
        enter_world      = 0x5f9f,
        do_sth           = 0x71bb,
        spawn            = 0x3858,
        move             = 0x15af,
        selected_character_spawn_data = 0x3ead,
        spawned_entity   = 0x392b,
        despawned_entity = 0x1393,
        world_update     = 0x5d15,
        self_world_update = 0x1e5c,
    };
}
