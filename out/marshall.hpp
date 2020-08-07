#include <inttypes.h>
#include <kumo/structs.hpp>
class client;
namespace kaminari
{
    class packet_reader;
}
namespace kaminari
{
    class packet
    {
        public:
        using ptr = boost::intrusive_ptr<packet>;
    };
}
namespace kumo
{
    void pack(const ::kaminari::packet::ptr& packet, const complex& data);
    uint8_t packet_size(const complex& data);
    void pack(const ::kaminari::packet::ptr& packet, const spawn_data& data);
    uint8_t packet_size(const spawn_data& data);
    uint8_t sizeof_spawn_data();
    bool unpack(::kaminari::packet_reader* packet, movement& data);
    uint8_t packet_size(const movement& data);
    uint8_t sizeof_movement();
    inline uint8_t sizeof_int8();
    inline uint8_t sizeof_int16();
    inline uint8_t sizeof_int32();
    inline uint8_t sizeof_int64();
    inline uint8_t sizeof_uint8();
    inline uint8_t sizeof_uint16();
    inline uint8_t sizeof_uint32();
    inline uint8_t sizeof_uint64();
    inline uint8_t sizeof_float();
    inline uint8_t sizeof_double();
    inline uint8_t sizeof_bool();
    bool handle_packet(::kaminari::packet_reader* packet, client* client);
}

namespace kumo
{
    inline uint8_t sizeof_int8()
    {
        return static_cast<uint8_t>(sizeof(int8_t));
    }
    inline uint8_t sizeof_int16()
    {
        return static_cast<uint8_t>(sizeof(int16_t));
    }
    inline uint8_t sizeof_int32()
    {
        return static_cast<uint8_t>(sizeof(int32_t));
    }
    inline uint8_t sizeof_int64()
    {
        return static_cast<uint8_t>(sizeof(int64_t));
    }
    inline uint8_t sizeof_uint8()
    {
        return static_cast<uint8_t>(sizeof(uint8_t));
    }
    inline uint8_t sizeof_uint16()
    {
        return static_cast<uint8_t>(sizeof(uint16_t));
    }
    inline uint8_t sizeof_uint32()
    {
        return static_cast<uint8_t>(sizeof(uint32_t));
    }
    inline uint8_t sizeof_uint64()
    {
        return static_cast<uint8_t>(sizeof(uint64_t));
    }
    inline uint8_t sizeof_float()
    {
        return static_cast<uint8_t>(sizeof(float));
    }
    inline uint8_t sizeof_double()
    {
        return static_cast<uint8_t>(sizeof(double));
    }
    inline uint8_t sizeof_bool()
    {
        return static_cast<uint8_t>(sizeof(bool));
    }
}
