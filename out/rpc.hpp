#pragma once
#include <kumo/opcodes.hpp>
#include <kumo/protocol_queues.hpp>
#include <kumo/structs.hpp>
#include <kaminari/buffers/packet.hpp>
#include <kaminari/broadcaster.hpp>
namespace kumo
{
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_handshake(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, client_handshake&& data, T&& callback);
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_handshake(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, client_handshake&& data);
    template <typename B, typename T>
    void broadcast_handshake(::kaminari::broadcaster<B>* broadcaster, client_handshake&& data, T&& callback);
    template <typename B>
    void broadcast_handshake(::kaminari::broadcaster<B>* broadcaster, client_handshake&& data);
    template <typename B, typename T>
    void broadcast_handshake_single(::kaminari::broadcaster<B>* broadcaster, client_handshake&& data, T&& callback);
    template <typename B>
    void broadcast_handshake_single(::kaminari::broadcaster<B>* broadcaster, client_handshake&& data);
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_login(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, login_data&& data, T&& callback);
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_login(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, login_data&& data);
    template <typename B, typename T>
    void broadcast_login(::kaminari::broadcaster<B>* broadcaster, login_data&& data, T&& callback);
    template <typename B>
    void broadcast_login(::kaminari::broadcaster<B>* broadcaster, login_data&& data);
    template <typename B, typename T>
    void broadcast_login_single(::kaminari::broadcaster<B>* broadcaster, login_data&& data, T&& callback);
    template <typename B>
    void broadcast_login_single(::kaminari::broadcaster<B>* broadcaster, login_data&& data);
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_character_selected(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_selection&& data, T&& callback);
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_character_selected(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_selection&& data);
    template <typename B, typename T>
    void broadcast_character_selected(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback);
    template <typename B>
    void broadcast_character_selected(::kaminari::broadcaster<B>* broadcaster, character_selection&& data);
    template <typename B, typename T>
    void broadcast_character_selected_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback);
    template <typename B>
    void broadcast_character_selected_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data);
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_move(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, movement&& data, T&& callback);
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_move(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, movement&& data);
    template <typename B, typename T>
    void broadcast_move(::kaminari::broadcaster<B>* broadcaster, movement&& data, T&& callback);
    template <typename B>
    void broadcast_move(::kaminari::broadcaster<B>* broadcaster, movement&& data);
    template <typename B, typename T>
    void broadcast_move_single(::kaminari::broadcaster<B>* broadcaster, movement&& data, T&& callback);
    template <typename B>
    void broadcast_move_single(::kaminari::broadcaster<B>* broadcaster, movement&& data);
}

namespace kumo
{
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_handshake(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, client_handshake&& data, T&& callback)
    {
        pq->send_reliable(opcode::handshake, std::move(data), std::forward<T>(callback));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_handshake(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, client_handshake&& data)
    {
        pq->send_reliable(opcode::handshake, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_handshake(::kaminari::broadcaster<B>* broadcaster, client_handshake&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::handshake, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B>
    void broadcast_handshake(::kaminari::broadcaster<B>* broadcaster, client_handshake&& data)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::handshake);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T>
    void broadcast_handshake_single(::kaminari::broadcaster<B>* broadcaster, client_handshake&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::handshake, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B>
    void broadcast_handshake_single(::kaminari::broadcaster<B>* broadcaster, client_handshake&& data)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::handshake);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_login(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, login_data&& data, T&& callback)
    {
        pq->send_reliable(opcode::login, std::move(data), std::forward<T>(callback));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_login(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, login_data&& data)
    {
        pq->send_reliable(opcode::login, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_login(::kaminari::broadcaster<B>* broadcaster, login_data&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::login, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B>
    void broadcast_login(::kaminari::broadcaster<B>* broadcaster, login_data&& data)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::login);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T>
    void broadcast_login_single(::kaminari::broadcaster<B>* broadcaster, login_data&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::login, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B>
    void broadcast_login_single(::kaminari::broadcaster<B>* broadcaster, login_data&& data)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::login);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_character_selected(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_selection&& data, T&& callback)
    {
        pq->send_reliable(opcode::character_selected, std::move(data), std::forward<T>(callback));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_character_selected(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_selection&& data)
    {
        pq->send_reliable(opcode::character_selected, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_character_selected(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::character_selected, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B>
    void broadcast_character_selected(::kaminari::broadcaster<B>* broadcaster, character_selection&& data)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::character_selected);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T>
    void broadcast_character_selected_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::character_selected, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B>
    void broadcast_character_selected_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::character_selected);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_move(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, movement&& data, T&& callback)
    {
        pq->send_ordered(opcode::move, std::move(data), std::forward<T>(callback));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_move(::kumo::protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, movement&& data)
    {
        pq->send_ordered(opcode::move, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_move(::kaminari::broadcaster<B>* broadcaster, movement&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::move, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B>
    void broadcast_move(::kaminari::broadcaster<B>* broadcaster, movement&& data)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::move);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename T>
    void broadcast_move_single(::kaminari::broadcaster<B>* broadcaster, movement&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::move, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B>
    void broadcast_move_single(::kaminari::broadcaster<B>* broadcaster, movement&& data)
    {
        boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::move);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
}
