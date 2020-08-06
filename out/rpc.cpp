#include "out/rpc.hpp"
namespace kaminari
{
    void send_do_sth(Client* client, complex&& data)
    {
        Packet::Ptr packet = Packet::make(opcode::do_sth);
        pack_complex(packet, data);
        ::kaminari::detail::send_reliable(client, packet);
    }
    void send_spawn(Client* client, spawn_data&& data)
    {
        Packet::Ptr packet = Packet::make(opcode::spawn);
        pack_spawn_data(packet, data);
        ::kaminari::detail::send_reliable(client, packet);
    }
}
