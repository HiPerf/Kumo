#pragma once
#include <optional>
#include <vector>
#include <string>
#include <inttypes.h>
namespace kumo
{
    struct client_handshake;
    struct status;
    struct login_data;
    struct status_ex;
    struct characters;
    struct character;
    struct character_selection;
    struct success;
    struct complex;
    struct has_id;
    struct spawn_data;
    struct movement;
    struct player_data;
    struct spawn;
    struct despawn;
    struct entity_update;
    struct world_update_data;
}

namespace kumo
{
    struct client_handshake
    {
    public:
        uint32_t version;
    };

    struct status
    {
    public:
        bool success;
    };

    struct login_data
    {
    public:
        std::string username;
        uint64_t password0;
        uint64_t password1;
        uint64_t password2;
        uint64_t password3;
    };

    struct status_ex
    {
    public:
        uint8_t code;
    };

    struct characters
    {
    public:
        std::vector<character> list;
    };

    struct character
    {
    public:
        std::string name;
        uint16_t level;
    };

    struct character_selection
    {
    public:
        uint8_t index;
    };

    struct success
    {
    };

    struct complex
    {
    public:
        std::optional<uint32_t> x;
        std::vector<spawn_data> y;
        int32_t z;
        std::optional<std::vector<bool>> w;
    };

    struct has_id
    {
    public:
        uint64_t id;
    };

    struct spawn_data
    {
    public:
        uint64_t id;
        int8_t x;
        int8_t y;
    };

    struct movement
    {
    public:
        int8_t direction;
    };

    struct player_data
    {
    public:
        uint64_t id;
        std::string name;
    };

    struct spawn
    {
    public:
        uint64_t id;
        float x;
        float z;
    };

    struct despawn
    {
    public:
        uint64_t id;
    };

    struct entity_update
    {
    public:
        uint64_t id;
        float x;
        float z;
        float angle;
    };

    struct world_update_data
    {
    public:
        std::vector<entity_update> data;
    };

}
