#include "out/rpc_detail.hpp"
class client;
template <typename B> class broadcaster;
namespace kaminari
{
    void send_do_sth(Client* client, complex&& data);
    template <typename T>
    void send_do_sth(Client* client, complex&& data, T&& callback);
    template <typename B>
    void broadcast_do_sth(broadcaster<B>* broadcaster, complex&& data);
    template <typename B, typename T>
    void broadcast_do_sth(broadcaster<B>* broadcaster, complex&& data, T&& callback);
    template <typename B>
    void broadcast_single_do_sth(broadcaster<B>* broadcaster, complex&& data);
    template <typename B, typename T>
    void broadcast_single_do_sth(broadcaster<B>* broadcaster, complex&& data, T&& callback);
    void send_spawn(Client* client, spawn_data&& data);
    template <typename T>
    void send_spawn(Client* client, spawn_data&& data, T&& callback);
    template <typename B>
    void broadcast_spawn(broadcaster<B>* broadcaster, spawn_data&& data);
    template <typename B, typename T>
    void broadcast_spawn(broadcaster<B>* broadcaster, spawn_data&& data, T&& callback);
    template <typename B>
    void broadcast_single_spawn(broadcaster<B>* broadcaster, spawn_data&& data);
    template <typename B, typename T>
    void broadcast_single_spawn(broadcaster<B>* broadcaster, spawn_data&& data, T&& callback);
}

namespace kaminari
{
    template <typename T>
    void send_do_sth(Client* client, complex&& data, T&& callback)
    {
        Packet::Ptr packet = Packet::make(opcode::do_sth, std::forward<T>(callback));
        pack_complex(packet, data);
        ::kaminari::detail::send_reliable(client, packet);
    }
    template <typename B>
    void broadcast_do_sth(broadcaster<B>* broadcaster, complex&& data)
    {
        Packet::Ptr packet = Packet::make(opcode::do_sth);
        pack_complex(packet, data);
        broadcaster->broadcast([packet](auto client) {
            ::kaminari::detail::send_reliable(client, packet);
        });
    }
    template <typename B, typename T>
    void broadcast_do_sth(broadcaster<B>* broadcaster, complex&& data, T&& callback)
    {
        Packet::Ptr packet = Packet::make(opcode::do_sth, std::forward<T>(callback));
        pack_complex(packet, data);
        broadcaster->broadcast([packet](auto client) {
            ::kaminari::detail::send_reliable(client, packet);
        });
    }
    template <typename B>
    void broadcast_single_do_sth(broadcaster<B>* broadcaster, complex&& data)
    {
        Packet::Ptr packet = Packet::make(opcode::do_sth);
        pack_complex(packet, data);
        broadcaster->broadcast_single([packet](auto client) {
            ::kaminari::detail::send_reliable(client, packet);
        });
    }
    template <typename B, typename T>
    void broadcast_single_do_sth(broadcaster<B>* broadcaster, complex&& data, T&& callback)
    {
        Packet::Ptr packet = Packet::make(opcode::do_sth, std::forward<T>(callback));
        pack_complex(packet, data);
        broadcaster->broadcast_single([packet](auto client) {
            ::kaminari::detail::send_reliable(client, packet);
        });
    }
    template <typename T>
    void send_spawn(Client* client, spawn_data&& data, T&& callback)
    {
        Packet::Ptr packet = Packet::make(opcode::spawn, std::forward<T>(callback));
        pack_spawn_data(packet, data);
        ::kaminari::detail::send_reliable(client, packet);
    }
    template <typename B>
    void broadcast_spawn(broadcaster<B>* broadcaster, spawn_data&& data)
    {
        Packet::Ptr packet = Packet::make(opcode::spawn);
        pack_spawn_data(packet, data);
        broadcaster->broadcast([packet](auto client) {
            ::kaminari::detail::send_reliable(client, packet);
        });
    }
    template <typename B, typename T>
    void broadcast_spawn(broadcaster<B>* broadcaster, spawn_data&& data, T&& callback)
    {
        Packet::Ptr packet = Packet::make(opcode::spawn, std::forward<T>(callback));
        pack_spawn_data(packet, data);
        broadcaster->broadcast([packet](auto client) {
            ::kaminari::detail::send_reliable(client, packet);
        });
    }
    template <typename B>
    void broadcast_single_spawn(broadcaster<B>* broadcaster, spawn_data&& data)
    {
        Packet::Ptr packet = Packet::make(opcode::spawn);
        pack_spawn_data(packet, data);
        broadcaster->broadcast_single([packet](auto client) {
            ::kaminari::detail::send_reliable(client, packet);
        });
    }
    template <typename B, typename T>
    void broadcast_single_spawn(broadcaster<B>* broadcaster, spawn_data&& data, T&& callback)
    {
        Packet::Ptr packet = Packet::make(opcode::spawn, std::forward<T>(callback));
        pack_spawn_data(packet, data);
        broadcaster->broadcast_single([packet](auto client) {
            ::kaminari::detail::send_reliable(client, packet);
        });
    }
}
