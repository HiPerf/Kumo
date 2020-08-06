#include "out/marshall.hpp"
#include "out/rpc.hpp"
namespace kumo
{
    void send_do_sth(client* client, complex&& data)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::do_sth);
        pack_complex(packet, data);
        ::kumo::detail::send_reliable(client, packet);
    }
    void send_spawn(client* client, spawn_data&& data)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::spawn);
        pack_spawn_data(packet, data);
        ::kumo::detail::send_reliable(client, packet);
    }
}
