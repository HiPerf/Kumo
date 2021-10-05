#pragma once
#include <inttypes.h>
#include <boost/intrusive_ptr.hpp>
#include <kumo/structs.hpp>
#include <kaminari/buffers/packet.hpp>
#include <kaminari/buffers/packet_reader.hpp>
#include <kaminari/cx/overflow.hpp>
#include "core/handler.hpp"
namespace kumo
{
    template <typename T>
    struct data_buffer;
    class marshal;
}

namespace kumo
{
    concept has_peek_move = requires(marshal m, position d);
    {
        { d.peek_move(nullptr, nullptr, d) } -> bool;
    }
    concept has_peek_login_character = requires(marshal m, character_selection d);
    {
        { d.peek_login_character(nullptr, nullptr, d) } -> bool;
    }
    concept has_peek_login = requires(marshal m, login_data d);
    {
        { d.peek_login(nullptr, nullptr, d) } -> bool;
    }
    concept has_peek_handshake = requires(marshal m, client_handshake d);
    {
        { d.peek_handshake(nullptr, nullptr, d) } -> bool;
    }
    concept has_peek_client_update = requires(marshal m, client_data d);
    {
        { d.peek_client_update(nullptr, nullptr, d) } -> bool;
    }
    concept has_peek_create_character = requires(marshal m, creation_data d);
    {
        { d.peek_create_character(nullptr, nullptr, d) } -> bool;
    }
    template <typename T>
    struct data_buffer
    {
    public:
        T data;
        uint16_t block_id;
        uint64_t timestamp;
    };

    class marshal:public handler
    {
    public:
        static bool unpack(::kaminari::buffers::packet_reader* packet, creation_data& data);
        static uint8_t packet_size(const creation_data& data);
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const character_selection& data);
        static uint8_t packet_size(const character_selection& data);
        static uint8_t sizeof_character_selection();
        static bool unpack(::kaminari::buffers::packet_reader* packet, client_data& data);
        static uint8_t packet_size(const client_data& data);
        static uint8_t sizeof_client_data();
        static bool unpack(::kaminari::buffers::packet_reader* packet, client_handshake& data);
        static uint8_t packet_size(const client_handshake& data);
        static uint8_t sizeof_client_handshake();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const status& data);
        static uint8_t packet_size(const status& data);
        static uint8_t sizeof_status();
        static bool unpack(::kaminari::buffers::packet_reader* packet, login_data& data);
        static uint8_t packet_size(const login_data& data);
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const status_ex& data);
        static uint8_t packet_size(const status_ex& data);
        static uint8_t sizeof_status_ex();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const characters_list_data& data);
        static uint8_t packet_size(const characters_list_data& data);
        static uint8_t sizeof_characters_list_data();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const character& data);
        static uint8_t packet_size(const character& data);
        static bool unpack(::kaminari::buffers::packet_reader* packet, character_selection& data);
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const success& data);
        static uint8_t packet_size(const success& data);
        static uint8_t sizeof_success();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const complex& data);
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const spawn_data& data);
        static uint8_t packet_size(const spawn_data& data);
        static uint8_t sizeof_spawn_data();
        static uint8_t packet_size(const complex& data);
        static bool unpack(::kaminari::buffers::packet_reader* packet, position& data);
        static uint8_t packet_size(const position& data);
        static uint8_t sizeof_position();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const character_spawn_data& data);
        static uint8_t packet_size(const character_spawn_data& data);
        static uint8_t sizeof_character_spawn_data();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const spawn& data);
        static uint8_t packet_size(const spawn& data);
        static uint8_t sizeof_spawn();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const despawn& data);
        static uint8_t packet_size(const despawn& data);
        static uint8_t sizeof_despawn();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const entity_update& data);
        static uint8_t packet_size(const entity_update& data);
        static uint8_t sizeof_entity_update();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const self_update& data);
        static uint8_t packet_size(const self_update& data);
        static uint8_t sizeof_self_update();
        static void pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const world_update_data& data);
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
        bool handle_packet(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id);
         marshal();
        void update(uint16_t block_id);
    protected:
        template <typename T>
        inline T& emplace_data(boost::circular_buffer<data_buffer<T>>& buffer, uint16_t block_id, uint64_t timestamp);
        template <typename T>
        inline bool check_buffer(boost::circular_buffer<data_buffer<T>>& buffer, uint16_t block_id, uint8_t buffer_size);
    private:
        template <typename C>
        bool handle_create_character(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id);
        template <typename C>
        bool handle_client_update(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id);
        template <typename C>
        bool handle_handshake(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id);
        template <typename C>
        bool handle_login(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id);
        template <typename C>
        bool handle_login_character(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id);
        template <typename C>
        bool handle_move(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id);
    private:
        boost::circular_buffer<::kumo::data_buffer<::kumo::creation_data>> _creation_data;
        uint8_t _creation_data_buffer_size;
        uint16_t _creation_data_last_peeked;
        uint16_t _creation_data_last_called;
        boost::circular_buffer<::kumo::data_buffer<::kumo::client_data>> _client_data;
        uint8_t _client_data_buffer_size;
        uint16_t _client_data_last_peeked;
        uint16_t _client_data_last_called;
        boost::circular_buffer<::kumo::data_buffer<::kumo::client_handshake>> _client_handshake;
        uint8_t _client_handshake_buffer_size;
        uint16_t _client_handshake_last_peeked;
        uint16_t _client_handshake_last_called;
        boost::circular_buffer<::kumo::data_buffer<::kumo::login_data>> _login_data;
        uint8_t _login_data_buffer_size;
        uint16_t _login_data_last_peeked;
        uint16_t _login_data_last_called;
        boost::circular_buffer<::kumo::data_buffer<::kumo::character_selection>> _character_selection;
        uint8_t _character_selection_buffer_size;
        uint16_t _character_selection_last_peeked;
        uint16_t _character_selection_last_called;
        boost::circular_buffer<::kumo::data_buffer<::kumo::position>> _position;
        uint8_t _position_buffer_size;
        uint16_t _position_last_peeked;
        uint16_t _position_last_called;
    };

    template <typename T>
    inline T& marshal::emplace_data(boost::circular_buffer<data_buffer<T>>& buffer, uint16_t block_id, uint64_t timestamp)
    {
        auto it = buffer.begin();
        while(it != buffer.end())
        {
            if (it->block_id > block_id)
            {
                break;
            }
            ++it;
        }
        return buffer.insert(it, { .block_id = block_id, .timestamp = timestamp })->data;
    }
    template <typename T>
    inline bool marshal::check_buffer(boost::circular_buffer<data_buffer<T>>& buffer, uint16_t block_id, uint8_t buffer_size)
    {
        return !buffer.empty() && cx::overflow::le(buffer.front().block_id, cx::overflow::sub(block_id, buffer_size));
    }
    template <typename C>
    bool marshal::handle_create_character(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id)
    {
        if (!check_client_status(client, ingame_status::in_world))
        {
            return handle_client_error(client, static_cast<::kumo::opcode>(packet->opcode()));
        }
        if (cx::overflow::leq(block_id, _create_character_last_called))
        {
            // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
            return true;
        }
        _create_character_last_called = block_id;
        auto& data = emplace_data(_creation_data, block_id, packet->timestamp());
        if (!unpack(packet, data))
        {
            return false;
        }
        if constexpr (has_peek_create_character);
        {
            if (cx::overflow::ge(block_id, _create_character_last_peeked))
            {
                _create_character_last_peeked = block_id;
                return peek_create_character(client, data, packet->timestamp());
            }
        }
        return true;
    }
    template <typename C>
    bool marshal::handle_client_update(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id)
    {
        if (cx::overflow::leq(block_id, _client_update_last_called))
        {
            // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
            return true;
        }
        _client_update_last_called = block_id;
        auto& data = emplace_data(_client_data, block_id, packet->timestamp());
        if (!unpack(packet, data))
        {
            return false;
        }
        if constexpr (has_peek_client_update);
        {
            if (cx::overflow::ge(block_id, _client_update_last_peeked))
            {
                _client_update_last_peeked = block_id;
                return peek_client_update(client, data, packet->timestamp());
            }
        }
        return true;
    }
    template <typename C>
    bool marshal::handle_handshake(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id)
    {
        if (!check_client_status(client, ingame_status::new_connection))
        {
            return handle_client_error(client, static_cast<::kumo::opcode>(packet->opcode()));
        }
        if (cx::overflow::leq(block_id, _handshake_last_called))
        {
            // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
            return true;
        }
        _handshake_last_called = block_id;
        auto& data = emplace_data(_client_handshake, block_id, packet->timestamp());
        if (!unpack(packet, data))
        {
            return false;
        }
        if constexpr (has_peek_handshake);
        {
            if (cx::overflow::ge(block_id, _handshake_last_peeked))
            {
                _handshake_last_peeked = block_id;
                return peek_handshake(client, data, packet->timestamp());
            }
        }
        return true;
    }
    template <typename C>
    bool marshal::handle_login(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id)
    {
        if (!check_client_status(client, ingame_status::handshake_done))
        {
            return handle_client_error(client, static_cast<::kumo::opcode>(packet->opcode()));
        }
        if (cx::overflow::leq(block_id, _login_last_called))
        {
            // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
            return true;
        }
        _login_last_called = block_id;
        auto& data = emplace_data(_login_data, block_id, packet->timestamp());
        if (!unpack(packet, data))
        {
            return false;
        }
        if constexpr (has_peek_login);
        {
            if (cx::overflow::ge(block_id, _login_last_peeked))
            {
                _login_last_peeked = block_id;
                return peek_login(client, data, packet->timestamp());
            }
        }
        return true;
    }
    template <typename C>
    bool marshal::handle_login_character(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id)
    {
        if (!check_client_status(client, ingame_status::login_done))
        {
            return handle_client_error(client, static_cast<::kumo::opcode>(packet->opcode()));
        }
        if (cx::overflow::leq(block_id, _login_character_last_called))
        {
            // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
            return true;
        }
        _login_character_last_called = block_id;
        auto& data = emplace_data(_character_selection, block_id, packet->timestamp());
        if (!unpack(packet, data))
        {
            return false;
        }
        if constexpr (has_peek_login_character);
        {
            if (cx::overflow::ge(block_id, _login_character_last_peeked))
            {
                _login_character_last_peeked = block_id;
                return peek_login_character(client, data, packet->timestamp());
            }
        }
        return true;
    }
    template <typename C>
    bool marshal::handle_move(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id)
    {
        if (!check_client_status(client, ingame_status::in_world))
        {
            return handle_client_error(client, static_cast<::kumo::opcode>(packet->opcode()));
        }
        if (cx::overflow::leq(block_id, _move_last_called))
        {
            // TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it
            return true;
        }
        _move_last_called = block_id;
        auto& data = emplace_data(_position, block_id, packet->timestamp());
        if (!unpack(packet, data))
        {
            return false;
        }
        if constexpr (has_peek_move);
        {
            if (cx::overflow::ge(block_id, _move_last_peeked))
            {
                _move_last_peeked = block_id;
                return peek_move(client, data, packet->timestamp());
            }
        }
        return true;
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
    bool marshal::handle_packet(C* client, ::kaminari::buffers::packet_reader* packet, uint16_t block_id)
    {
        switch (static_cast<::kumo::opcode>(packet->opcode()))
        {
            case opcode::login:
                return handle_login(client, packet, block_id);
            case opcode::move:
                return handle_move(client, packet, block_id);
            case opcode::login_character:
                return handle_login_character(client, packet, block_id);
            case opcode::create_character:
                return handle_create_character(client, packet, block_id);
            case opcode::handshake:
                return handle_handshake(client, packet, block_id);
            case opcode::client_update:
                return handle_client_update(client, packet, block_id);
            default:
                return false;
        }
    }
}
