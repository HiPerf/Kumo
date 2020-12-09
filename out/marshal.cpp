#include <kumo/opcodes.hpp>
#include <kumo/marshal.hpp>
#include <kaminari/buffers/packet_reader.hpp>
namespace kumo
{
    void marshal::pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const complex& data)
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
    void marshal::pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const spawn_data& data)
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
    bool marshal::unpack(::kaminari::packet_reader* packet, movement& data)
    {
        if (packet->bytes_read() + sizeof_int8() > packet->buffer_size())
        {
            return false;
        }
        data.direction = packet->read<int8_t>();
        return true;
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
}
