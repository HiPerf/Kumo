#pragma once
#include <inttypes.h>
#include <boost/intrusive_ptr.hpp>
#include <kumo/structs.hpp>
class client;
namespace kaminari
{
    class packet_reader;
}
namespace kaminari
{
    class packet;
}
namespace kumo
{
    class marshal;
}

namespace kumo
{
    class marshal
    {
    public:
        static void pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const complex& data);
        static uint8_t packet_size(const complex& data);
        static void pack(const boost::intrusive_ptr<::kaminari::packet>& packet, const spawn_data& data);
        static uint8_t packet_size(const spawn_data& data);
        static uint8_t sizeof_spawn_data();
        static bool unpack(::kaminari::packet_reader* packet, movement& data);
        static uint8_t packet_size(const movement& data);
        static uint8_t sizeof_movement();
        inline static uint8_t sizeof_int8();
        inline static uint8_t sizeof_int16();
        inline static uint8_t sizeof_int32();
        inline static uint8_t sizeof_int64();
        inline static uint8_t sizeof_uint8();
        inline static uint8_t sizeof_uint16();
        inline static uint8_t sizeof_uint32();
        inline static uint8_t sizeof_uint64();
        inline static uint8_t sizeof_float();
        inline static uint8_t sizeof_double();
        inline static uint8_t sizeof_bool();
    private:
        static bool handle_packet(::kaminari::packet_reader* packet, client* client);
    };

    inline uint8_t marshal::sizeof_int8()
    {
        return static_cast<uint8_t>(sizeof(int8_t));
    }
    inline uint8_t marshal::sizeof_int16()
    {
        return static_cast<uint8_t>(sizeof(int16_t));
    }
    inline uint8_t marshal::sizeof_int32()
    {
        return static_cast<uint8_t>(sizeof(int32_t));
    }
    inline uint8_t marshal::sizeof_int64()
    {
        return static_cast<uint8_t>(sizeof(int64_t));
    }
    inline uint8_t marshal::sizeof_uint8()
    {
        return static_cast<uint8_t>(sizeof(uint8_t));
    }
    inline uint8_t marshal::sizeof_uint16()
    {
        return static_cast<uint8_t>(sizeof(uint16_t));
    }
    inline uint8_t marshal::sizeof_uint32()
    {
        return static_cast<uint8_t>(sizeof(uint32_t));
    }
    inline uint8_t marshal::sizeof_uint64()
    {
        return static_cast<uint8_t>(sizeof(uint64_t));
    }
    inline uint8_t marshal::sizeof_float()
    {
        return static_cast<uint8_t>(sizeof(float));
    }
    inline uint8_t marshal::sizeof_double()
    {
        return static_cast<uint8_t>(sizeof(double));
    }
    inline uint8_t marshal::sizeof_bool()
    {
        return static_cast<uint8_t>(sizeof(bool));
    }
}
