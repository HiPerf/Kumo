#include "out/opcodes.hpp"
#include "out/rpc_detail.hpp"
#include "out/structs.hpp"
#include <kaminari/buffers/packet.hpp>
#include <kaminari/broadcaster.hpp>
class client;
namespace kumo
{
    void send_do_sth(client* client, complex&& data);
    template <typename T>
    void send_do_sth(client* client, complex&& data, T&& callback);
    template <typename B>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data);
    template <typename B, typename T>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback);
    template <typename B>
    void broadcast_single_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data);
    template <typename B, typename T>
    void broadcast_single_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback);
    void send_spawn(client* client, spawn_data&& data);
    template <typename T>
    void send_spawn(client* client, spawn_data&& data, T&& callback);
    template <typename B>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data);
    template <typename B, typename T>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback);
    template <typename B>
    void broadcast_single_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data);
    template <typename B, typename T>
    void broadcast_single_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback);
}

namespace kumo
{
    template <typename T>
    void send_do_sth(client* client, complex&& data, T&& callback)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::do_sth, std::forward<T>(callback));
        pack_complex(packet, data);
        ::kumo::detail::send_reliable(client, packet);
    }
    template <typename B>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::do_sth);
        pack_complex(packet, data);
        broadcaster->broadcast([packet](auto client) {
            ::kumo::detail::send_reliable(client, packet);
        });
    }
    template <typename B, typename T>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::do_sth, std::forward<T>(callback));
        pack_complex(packet, data);
        broadcaster->broadcast([packet](auto client) {
            ::kumo::detail::send_reliable(client, packet);
        });
    }
    template <typename B>
    void broadcast_single_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::do_sth);
        pack_complex(packet, data);
        broadcaster->broadcast_single([packet](auto client) {
            ::kumo::detail::send_reliable(client, packet);
        });
    }
    template <typename B, typename T>
    void broadcast_single_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::do_sth, std::forward<T>(callback));
        pack_complex(packet, data);
        broadcaster->broadcast_single([packet](auto client) {
            ::kumo::detail::send_reliable(client, packet);
        });
    }
    template <typename T>
    void send_spawn(client* client, spawn_data&& data, T&& callback)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::spawn, std::forward<T>(callback));
        pack_spawn_data(packet, data);
        ::kumo::detail::send_reliable(client, packet);
    }
    template <typename B>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::spawn);
        pack_spawn_data(packet, data);
        broadcaster->broadcast([packet](auto client) {
            ::kumo::detail::send_reliable(client, packet);
        });
    }
    template <typename B, typename T>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::spawn, std::forward<T>(callback));
        pack_spawn_data(packet, data);
        broadcaster->broadcast([packet](auto client) {
            ::kumo::detail::send_reliable(client, packet);
        });
    }
    template <typename B>
    void broadcast_single_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::spawn);
        pack_spawn_data(packet, data);
        broadcaster->broadcast_single([packet](auto client) {
            ::kumo::detail::send_reliable(client, packet);
        });
    }
    template <typename B, typename T>
    void broadcast_single_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback)
    {
        ::kaminari::packet::ptr packet = ::kaminari::packet::make(opcode::spawn, std::forward<T>(callback));
        pack_spawn_data(packet, data);
        broadcaster->broadcast_single([packet](auto client) {
            ::kumo::detail::send_reliable(client, packet);
        });
    }
}
