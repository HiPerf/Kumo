#include <kumo/opcodes.hpp>
#include <kumo/marshal.hpp>
#include <kaminari/buffers/packet_reader.hpp>
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
    bool marshal::unpack(::kaminari::buffers::packet_reader* packet, creation_data& data)
    {
        if (packet->bytes_read() + sizeof_uint8() > packet->buffer_size())
        {
            return false;
        }
        if (packet->bytes_read() + sizeof_uint8() + packet->peek<uint8_t>() > packet->buffer_size())
        {
            return false;
        }
        data.name = packet->read<std::string>();
        return true;
    }
    uint8_t marshal::packet_size(const creation_data& data)
    {
        uint8_t size = 0;
        size += sizeof_uint8() + data.name.length();
        return size;
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const character_selection& data)
    {
        *packet << data.index;
    }
    uint8_t marshal::packet_size(const character_selection& data)
    {
        (void)data;
        return sizeof(character_selection);
    }
    uint8_t marshal::sizeof_character_selection()
    {
        return sizeof(character_selection);
    }
    bool marshal::unpack(::kaminari::buffers::packet_reader* packet, client_data& data)
    {
        if (packet->bytes_read() + sizeof_int8() > packet->buffer_size())
        {
            return false;
        }
        data.x = packet->read<int8_t>();
        if (packet->bytes_read() + sizeof_int8() > packet->buffer_size())
        {
            return false;
        }
        data.y = packet->read<int8_t>();
        if (packet->bytes_read() + sizeof_uint8() > packet->buffer_size())
        {
            return false;
        }
        data.seq = packet->read<uint8_t>();
        return true;
    }
    uint8_t marshal::packet_size(const client_data& data)
    {
        (void)data;
        return sizeof(client_data);
    }
    uint8_t marshal::sizeof_client_data()
    {
        return sizeof(client_data);
    }
    bool marshal::unpack(::kaminari::buffers::packet_reader* packet, client_handshake& data)
    {
        if (packet->bytes_read() + sizeof_uint32() > packet->buffer_size())
        {
            return false;
        }
        data.version = packet->read<uint32_t>();
        return true;
    }
    uint8_t marshal::packet_size(const client_handshake& data)
    {
        (void)data;
        return sizeof(client_handshake);
    }
    uint8_t marshal::sizeof_client_handshake()
    {
        return sizeof(client_handshake);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const status& data)
    {
        *packet << data.success;
    }
    uint8_t marshal::packet_size(const status& data)
    {
        (void)data;
        return sizeof(status);
    }
    uint8_t marshal::sizeof_status()
    {
        return sizeof(status);
    }
    bool marshal::unpack(::kaminari::buffers::packet_reader* packet, login_data& data)
    {
        if (packet->bytes_read() + sizeof_uint8() > packet->buffer_size())
        {
            return false;
        }
        if (packet->bytes_read() + sizeof_uint8() + packet->peek<uint8_t>() > packet->buffer_size())
        {
            return false;
        }
        data.username = packet->read<std::string>();
        if (packet->bytes_read() + sizeof_uint64() > packet->buffer_size())
        {
            return false;
        }
        data.password0 = packet->read<uint64_t>();
        if (packet->bytes_read() + sizeof_uint64() > packet->buffer_size())
        {
            return false;
        }
        data.password1 = packet->read<uint64_t>();
        if (packet->bytes_read() + sizeof_uint64() > packet->buffer_size())
        {
            return false;
        }
        data.password2 = packet->read<uint64_t>();
        if (packet->bytes_read() + sizeof_uint64() > packet->buffer_size())
        {
            return false;
        }
        data.password3 = packet->read<uint64_t>();
        return true;
    }
    uint8_t marshal::packet_size(const login_data& data)
    {
        uint8_t size = 0;
        size += sizeof_uint8() + data.username.length();
        size += sizeof_uint64();
        size += sizeof_uint64();
        size += sizeof_uint64();
        size += sizeof_uint64();
        return size;
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const status_ex& data)
    {
        *packet << data.code;
    }
    uint8_t marshal::packet_size(const status_ex& data)
    {
        (void)data;
        return sizeof(status_ex);
    }
    uint8_t marshal::sizeof_status_ex()
    {
        return sizeof(status_ex);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const characters_list_data& data)
    {
        *packet << data.num_characters;
    }
    uint8_t marshal::packet_size(const characters_list_data& data)
    {
        (void)data;
        return sizeof(characters_list_data);
    }
    uint8_t marshal::sizeof_characters_list_data()
    {
        return sizeof(characters_list_data);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const character& data)
    {
        *packet << data.name;
        *packet << data.level;
    }
    uint8_t marshal::packet_size(const character& data)
    {
        uint8_t size = 0;
        size += sizeof_uint8() + data.name.length();
        size += sizeof_uint16();
        return size;
    }
    bool marshal::unpack(::kaminari::buffers::packet_reader* packet, character_selection& data)
    {
        if (packet->bytes_read() + sizeof_uint8() > packet->buffer_size())
        {
            return false;
        }
        data.index = packet->read<uint8_t>();
        return true;
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const success& data)
    {
    }
    uint8_t marshal::packet_size(const success& data)
    {
        (void)data;
        return sizeof(success);
    }
    uint8_t marshal::sizeof_success()
    {
        return sizeof(success);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const complex& data)
    {
        *packet << static_cast<bool>(data.x);
        if (static_cast<bool>(data.x))
        {
            *packet << *data.x;
        }
        *packet << static_cast<uint8_t>((data.y).size());
        for (const spawn_data& val : data.y)
        {
            pack(packet, val);
        }
        *packet << data.z;
        *packet << static_cast<bool>(data.w);
        if (static_cast<bool>(data.w))
        {
            *packet << static_cast<uint8_t>((*data.w).size());
            for (const bool& val : *data.w)
            {
                *packet << val;
            }
        }
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const spawn_data& data)
    {
        *packet << data.id;
        *packet << data.x;
        *packet << data.y;
    }
    uint8_t marshal::packet_size(const spawn_data& data)
    {
        (void)data;
        return sizeof(spawn_data);
    }
    uint8_t marshal::sizeof_spawn_data()
    {
        return sizeof(spawn_data);
    }
    uint8_t marshal::packet_size(const complex& data)
    {
        uint8_t size = 0;
        size += sizeof(bool);
        if (static_cast<bool>(data.x))
        {
            size += sizeof_uint32();
        }
        size += sizeof(uint8_t) + (data.y).size() * sizeof_spawn_data();
        size += sizeof_int32();
        size += sizeof(bool);
        if (static_cast<bool>(data.w))
        {
            size += sizeof(uint8_t) + (*data.w).size() * sizeof_bool();
        }
        return size;
    }
    bool marshal::unpack(::kaminari::buffers::packet_reader* packet, position& data)
    {
        if (packet->bytes_read() + sizeof_uint64() > packet->buffer_size())
        {
            return false;
        }
        data.id = packet->read<uint64_t>();
        if (packet->bytes_read() + sizeof_float() > packet->buffer_size())
        {
            return false;
        }
        data.x = packet->read<float>();
        if (packet->bytes_read() + sizeof_float() > packet->buffer_size())
        {
            return false;
        }
        data.z = packet->read<float>();
        return true;
    }
    uint8_t marshal::packet_size(const position& data)
    {
        (void)data;
        return sizeof(position);
    }
    uint8_t marshal::sizeof_position()
    {
        return sizeof(position);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const character_spawn_data& data)
    {
        *packet << data.id;
    }
    uint8_t marshal::packet_size(const character_spawn_data& data)
    {
        (void)data;
        return sizeof(character_spawn_data);
    }
    uint8_t marshal::sizeof_character_spawn_data()
    {
        return sizeof(character_spawn_data);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const spawn& data)
    {
        *packet << data.id;
        *packet << data.type;
        *packet << data.x;
        *packet << data.z;
    }
    uint8_t marshal::packet_size(const spawn& data)
    {
        (void)data;
        return sizeof(spawn);
    }
    uint8_t marshal::sizeof_spawn()
    {
        return sizeof(spawn);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const despawn& data)
    {
        *packet << data.id;
    }
    uint8_t marshal::packet_size(const despawn& data)
    {
        (void)data;
        return sizeof(despawn);
    }
    uint8_t marshal::sizeof_despawn()
    {
        return sizeof(despawn);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const entity_update& data)
    {
        *packet << data.id;
        *packet << data.x;
        *packet << data.z;
        *packet << data.speed;
        *packet << data.vx;
        *packet << data.vz;
    }
    uint8_t marshal::packet_size(const entity_update& data)
    {
        (void)data;
        return sizeof(entity_update);
    }
    uint8_t marshal::sizeof_entity_update()
    {
        return sizeof(entity_update);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const self_update& data)
    {
        *packet << data.x;
        *packet << data.z;
        *packet << data.speed;
        *packet << data.vx;
        *packet << data.vz;
        *packet << data.seq;
        *packet << data.frame;
    }
    uint8_t marshal::packet_size(const self_update& data)
    {
        (void)data;
        return sizeof(self_update);
    }
    uint8_t marshal::sizeof_self_update()
    {
        return sizeof(self_update);
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::buffers::packet>& packet, const world_update_data& data)
    {
        *packet << static_cast<uint8_t>((data.data).size());
        for (const entity_update& val : data.data)
        {
            pack(packet, val);
        }
    }
    uint8_t marshal::packet_size(const world_update_data& data)
    {
        uint8_t size = 0;
        size += sizeof(uint8_t) + (data.data).size() * sizeof_entity_update();
        return size;
    }
     marshal::marshal():
        _create_character(4),
        _create_character_buffer_size(2),
        _create_character_last_peeked(0),
        _create_character_last_called(0),
        _client_update(4),
        _client_update_buffer_size(2),
        _client_update_last_peeked(0),
        _client_update_last_called(0),
        _handshake(4),
        _handshake_buffer_size(2),
        _handshake_last_peeked(0),
        _handshake_last_called(0),
        _login(4),
        _login_buffer_size(2),
        _login_last_peeked(0),
        _login_last_called(0),
        _login_character(4),
        _login_character_buffer_size(2),
        _login_character_last_peeked(0),
        _login_character_last_called(0),
        _move(4),
        _move_buffer_size(2),
        _move_last_peeked(0),
        _move_last_called(0)
    {
    }
    void marshal::update(uint16_t block_id)
    {
        while (check_buffer(_create_character, block_id, _create_character_buffer_size))
        {
            on_create_character(client, _create_character.front().data, _create_character.front().timestamp);
            create_character.pop_front();
        }
        while (check_buffer(_client_update, block_id, _client_update_buffer_size))
        {
            on_client_update(client, _client_update.front().data, _client_update.front().timestamp);
            client_update.pop_front();
        }
        while (check_buffer(_handshake, block_id, _handshake_buffer_size))
        {
            on_handshake(client, _handshake.front().data, _handshake.front().timestamp);
            handshake.pop_front();
        }
        while (check_buffer(_login, block_id, _login_buffer_size))
        {
            on_login(client, _login.front().data, _login.front().timestamp);
            login.pop_front();
        }
        while (check_buffer(_login_character, block_id, _login_character_buffer_size))
        {
            on_login_character(client, _login_character.front().data, _login_character.front().timestamp);
            login_character.pop_front();
        }
        while (check_buffer(_move, block_id, _move_buffer_size))
        {
            on_move(client, _move.front().data, _move.front().timestamp);
            move.pop_front();
        }
    }
}
