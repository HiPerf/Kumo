#include <kumo/opcodes.hpp>
#include <kumo/marshal.hpp>
#include <kaminari/buffers/packet_reader.hpp>
namespace kumo
{
    void marshal::pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const client_handshake& data)
    {
        *packet << data.version;
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
    bool marshal::unpack(::kaminari::packet_reader* packet, status& data)
    {
        if (packet->bytes_read() + sizeof_bool() > packet->buffer_size())
        {
            return false;
        }
        data.success = packet->read<bool>();
        return true;
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
    void marshal::pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const login_data& data)
    {
        *packet << data.username;
        *packet << data.password0;
        *packet << data.password1;
        *packet << data.password2;
        *packet << data.password3;
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
    bool marshal::unpack(::kaminari::packet_reader* packet, status_ex& data)
    {
        if (packet->bytes_read() + sizeof_uint8() > packet->buffer_size())
        {
            return false;
        }
        data.code = packet->read<uint8_t>();
        return true;
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
    bool marshal::unpack(::kaminari::packet_reader* packet, characters& data)
    {
        uint8_t size = packet->read<uint8_t>();
        for (int i = 0; i < size; ++i)
        {
            character data;
            if (unpack(packet, data)
            {
                (data.list).push_back(std::move(data));
            }
            else;
            {
                return false;
            }
        }
        return true;
    }
    bool marshal::unpack(::kaminari::packet_reader* packet, character& data)
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
        if (packet->bytes_read() + sizeof_uint16() > packet->buffer_size())
        {
            return false;
        }
        data.level = packet->read<uint16_t>();
        return true;
    }
    uint8_t marshal::packet_size(const character& data)
    {
        uint8_t size = 0;
        size += sizeof_uint8() + data.name.length();
        size += sizeof_uint16();
        return size;
    }
    uint8_t marshal::packet_size(const characters& data)
    {
        uint8_t size = 0;
        size += sizeof(uint8_t);
        for (const character& val : data.list)
        {
            size += packet_size(val);
        }
        return size;
    }
    void marshal::pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const character_selection& data)
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
    bool marshal::unpack(::kaminari::packet_reader* packet, success& data)
    {
        return true;
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
    bool marshal::unpack(::kaminari::packet_reader* packet, complex& data)
    {
        if (packet->bytes_read() + sizeof(bool) > packet->buffer_size())
        {
            return false;
        }
        if (packet->read<uint8_t>() == 1)
        {
            if (packet->bytes_read() + sizeof_uint32() > packet->buffer_size())
            {
                return false;
            }
            *data.x = packet->read<uint32_t>();
        }
        uint8_t size = packet->read<uint8_t>();
        for (int i = 0; i < size; ++i)
        {
            spawn_data data;
            if (unpack(packet, data)
            {
                (data.y).push_back(std::move(data));
            }
            else;
            {
                return false;
            }
        }
        if (packet->bytes_read() + sizeof_int32() > packet->buffer_size())
        {
            return false;
        }
        data.z = packet->read<int32_t>();
        if (packet->bytes_read() + sizeof(bool) > packet->buffer_size())
        {
            return false;
        }
        if (packet->read<uint8_t>() == 1)
        {
            uint8_t size = packet->read<uint8_t>();
            if (packet->bytes_read() + size * sizeof_bool() > packet->buffer_size())
            {
                return false;
            }
            for (int i = 0; i < size; ++i)
            {
                (*data.w).push_back(packet->read<bool>());
            }
        }
        return true;
    }
    bool marshal::unpack(::kaminari::packet_reader* packet, spawn_data& data)
    {
        if (packet->bytes_read() + sizeof_uint64() > packet->buffer_size())
        {
            return false;
        }
        data.id = packet->read<uint64_t>();
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
        return true;
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
    void marshal::pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const movement& data)
    {
        *packet << data.direction;
    }
    uint8_t marshal::packet_size(const movement& data)
    {
        (void)data;
        return sizeof(movement);
    }
    uint8_t marshal::sizeof_movement()
    {
        return sizeof(movement);
    }
    bool marshal::unpack(::kaminari::packet_reader* packet, player_data& data)
    {
        if (packet->bytes_read() + sizeof_uint64() > packet->buffer_size())
        {
            return false;
        }
        data.id = packet->read<uint64_t>();
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
    uint8_t marshal::packet_size(const player_data& data)
    {
        uint8_t size = 0;
        size += sizeof_uint64();
        size += sizeof_uint8() + data.name.length();
        return size;
    }
    bool marshal::unpack(::kaminari::packet_reader* packet, spawn& data)
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
    uint8_t marshal::packet_size(const spawn& data)
    {
        (void)data;
        return sizeof(spawn);
    }
    uint8_t marshal::sizeof_spawn()
    {
        return sizeof(spawn);
    }
    bool marshal::unpack(::kaminari::packet_reader* packet, despawn& data)
    {
        if (packet->bytes_read() + sizeof_uint64() > packet->buffer_size())
        {
            return false;
        }
        data.id = packet->read<uint64_t>();
        return true;
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
    bool marshal::unpack(::kaminari::packet_reader* packet, entity_update& data)
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
        if (packet->bytes_read() + sizeof_float() > packet->buffer_size())
        {
            return false;
        }
        data.angle = packet->read<float>();
        return true;
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
    void marshal::pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const world_update_data& data)
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
}
