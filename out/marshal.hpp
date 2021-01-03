#pragma once
#include <inttypes.h>
#include <boost/intrusive_ptr.hpp>
#include <kumo/structs.hpp>
#include <kaminari/buffers/packet.hpp>
#include <kaminari/buffers/packet_reader.hpp>
#include "core/handler.hpp"
namespace kumo
{
    class marshal;
}

namespace kumo
{
    class marshal:public handler
    {
    public:
        static void pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const client_handshake& data);
        static uint8_t packet_size(const client_handshake& data);
        static uint8_t sizeof_client_handshake();
        static bool unpack(::kaminari::packet_reader* packet, status& data);
        static uint8_t packet_size(const status& data);
        static uint8_t sizeof_status();
        static void pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const login_data& data);
        static uint8_t packet_size(const login_data& data);
        static bool unpack(::kaminari::packet_reader* packet, status_ex& data);
        static uint8_t packet_size(const status_ex& data);
        static uint8_t sizeof_status_ex();
        static bool unpack(::kaminari::packet_reader* packet, characters& data);
        static bool unpack(::kaminari::packet_reader* packet, character& data);
        static uint8_t packet_size(const character& data);
        static uint8_t packet_size(const characters& data);
        static void pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const character_selection& data);
        static uint8_t packet_size(const character_selection& data);
        static uint8_t sizeof_character_selection();
        static bool unpack(::kaminari::packet_reader* packet, success& data);
        static uint8_t packet_size(const success& data);
        static uint8_t sizeof_success();
        static bool unpack(::kaminari::packet_reader* packet, complex& data);
        static bool unpack(::kaminari::packet_reader* packet, spawn_data& data);
        static uint8_t packet_size(const spawn_data& data);
        static uint8_t sizeof_spawn_data();
        static uint8_t packet_size(const complex& data);
        static void pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const movement& data);
        static uint8_t packet_size(const movement& data);
        static uint8_t sizeof_movement();
        static bool unpack(::kaminari::packet_reader* packet, player_data& data);
        static uint8_t packet_size(const player_data& data);
        static bool unpack(::kaminari::packet_reader* packet, spawn& data);
        static uint8_t packet_size(const spawn& data);
        static uint8_t sizeof_spawn();
        static bool unpack(::kaminari::packet_reader* packet, despawn& data);
        static uint8_t packet_size(const despawn& data);
        static uint8_t sizeof_despawn();
        static bool unpack(::kaminari::packet_reader* packet, entity_update& data);
        static uint8_t packet_size(const entity_update& data);
        static uint8_t sizeof_entity_update();
        static void pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const world_update_data& data);
        static uint8_t packet_size(const world_update_data& data);
        inline constexpr static uint8_t sizeof_int8();
        inline constexpr static uint8_t sizeof_int16();
        inline constexpr static uint8_t sizeof_int32();
        inline constexpr static uint8_t sizeof_int64();
        inline constexpr static uint8_t sizeof_uint8();
        inline constexpr static uint8_t sizeof_uint16();
        inline constexpr static uint8_t sizeof_uint32();
        inline constexpr static uint8_t sizeof_uint64();
        inline constexpr static uint8_t sizeof_float();
        inline constexpr static uint8_t sizeof_double();
        inline constexpr static uint8_t sizeof_bool();
        template <typename C>
        static bool handle_packet(::kaminari::packet_reader* packet, C* client);
    private:
        template <typename C>
        static bool handle_handshake_response(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_login_response(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_characters_list(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_enter_world(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_do_sth(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_spawn(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_player_information(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_spawned_entity(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_despawned_entity(::kaminari::packet_reader* packet, C* client);
        template <typename C>
        static bool handle_world_update(::kaminari::packet_reader* packet, C* client);
    };

    template <typename C>
    bool marshal::handle_handshake_response(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::status data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_handshake_response(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_login_response(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::status_ex data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_login_response(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_characters_list(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::characters data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_characters_list(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_enter_world(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::success data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_enter_world(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_do_sth(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::complex data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_do_sth(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_spawn(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::spawn_data data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_spawn(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_player_information(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::player_data data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_player_information(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_spawned_entity(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::spawn data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_spawned_entity(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_despawned_entity(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::despawn data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_despawned_entity(client, data, packet->timestamp());
    }
    template <typename C>
    bool marshal::handle_world_update(::kaminari::packet_reader* packet, C* client)
    {
        ::kumo::entity_update data;
        if (!unpack(packet, data))
        {
            return false;
        }
        return on_world_update(client, data, packet->timestamp());
    }
    inline constexpr uint8_t marshal::sizeof_int8()
    {
        return static_cast<uint8_t>(sizeof(int8_t));
    }
    inline constexpr uint8_t marshal::sizeof_int16()
    {
        return static_cast<uint8_t>(sizeof(int16_t));
    }
    inline constexpr uint8_t marshal::sizeof_int32()
    {
        return static_cast<uint8_t>(sizeof(int32_t));
    }
    inline constexpr uint8_t marshal::sizeof_int64()
    {
        return static_cast<uint8_t>(sizeof(int64_t));
    }
    inline constexpr uint8_t marshal::sizeof_uint8()
    {
        return static_cast<uint8_t>(sizeof(uint8_t));
    }
    inline constexpr uint8_t marshal::sizeof_uint16()
    {
        return static_cast<uint8_t>(sizeof(uint16_t));
    }
    inline constexpr uint8_t marshal::sizeof_uint32()
    {
        return static_cast<uint8_t>(sizeof(uint32_t));
    }
    inline constexpr uint8_t marshal::sizeof_uint64()
    {
        return static_cast<uint8_t>(sizeof(uint64_t));
    }
    inline constexpr uint8_t marshal::sizeof_float()
    {
        return static_cast<uint8_t>(sizeof(float));
    }
    inline constexpr uint8_t marshal::sizeof_double()
    {
        return static_cast<uint8_t>(sizeof(double));
    }
    inline constexpr uint8_t marshal::sizeof_bool()
    {
        return static_cast<uint8_t>(sizeof(bool));
    }
    template <typename C>
    bool marshal::handle_packet(::kaminari::packet_reader* packet, C* client)
    {
        switch (static_cast<::kumo::opcode>(packet->opcode()))
        {
            case opcode::enter_world:
                return handle_enter_world(packet, client);
            case opcode::login_response:
                return handle_login_response(packet, client);
            case opcode::player_information:
                return handle_player_information(packet, client);
            case opcode::spawned_entity:
                return handle_spawned_entity(packet, client);
            case opcode::do_sth:
                return handle_do_sth(packet, client);
            case opcode::world_update:
                return handle_world_update(packet, client);
            case opcode::despawned_entity:
                return handle_despawned_entity(packet, client);
            case opcode::characters_list:
                return handle_characters_list(packet, client);
            case opcode::spawn:
                return handle_spawn(packet, client);
            case opcode::handshake_response:
                return handle_handshake_response(packet, client);
            default:
                return false;
        }
    }
}
