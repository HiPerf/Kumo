#pragma once
#include <kumo/opcodes.hpp>
#include <kumo/protocol_queues.hpp>
#include <kumo/structs.hpp>
#include <kaminari/buffers/packet.hpp>
#include <kaminari/broadcaster.hpp>
namespace kumo
{
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_character_created(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_selection&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_character_created(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_selection&& data);
    template <typename B, typename T>
    void broadcast_character_created(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_character_created(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_character_created(::kaminari::broadcaster<B>* broadcaster, character_selection&& data);
    template <typename B, typename D>
    void broadcast_character_created(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_character_created_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_character_created_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_character_created_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data);
    template <typename B, typename D>
    void broadcast_character_created_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_handshake_response(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_handshake_response(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status&& data);
    template <typename B, typename T>
    void broadcast_handshake_response(::kaminari::broadcaster<B>* broadcaster, status&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_handshake_response(::kaminari::broadcaster<B>* broadcaster, status&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_handshake_response(::kaminari::broadcaster<B>* broadcaster, status&& data);
    template <typename B, typename D>
    void broadcast_handshake_response(::kaminari::broadcaster<B>* broadcaster, status&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_handshake_response_single(::kaminari::broadcaster<B>* broadcaster, status&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_handshake_response_single(::kaminari::broadcaster<B>* broadcaster, status&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_handshake_response_single(::kaminari::broadcaster<B>* broadcaster, status&& data);
    template <typename B, typename D>
    void broadcast_handshake_response_single(::kaminari::broadcaster<B>* broadcaster, status&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_login_response(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status_ex&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_login_response(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status_ex&& data);
    template <typename B, typename T>
    void broadcast_login_response(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_login_response(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_login_response(::kaminari::broadcaster<B>* broadcaster, status_ex&& data);
    template <typename B, typename D>
    void broadcast_login_response(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_login_response_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_login_response_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_login_response_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data);
    template <typename B, typename D>
    void broadcast_login_response_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_characters_list(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, characters_list_data&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_characters_list(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, characters_list_data&& data);
    template <typename B, typename T>
    void broadcast_characters_list(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_characters_list(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_characters_list(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data);
    template <typename B, typename D>
    void broadcast_characters_list(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_characters_list_single(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_characters_list_single(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_characters_list_single(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data);
    template <typename B, typename D>
    void broadcast_characters_list_single(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_character_information(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_character_information(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character&& data);
    template <typename B, typename T>
    void broadcast_character_information(::kaminari::broadcaster<B>* broadcaster, character&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_character_information(::kaminari::broadcaster<B>* broadcaster, character&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_character_information(::kaminari::broadcaster<B>* broadcaster, character&& data);
    template <typename B, typename D>
    void broadcast_character_information(::kaminari::broadcaster<B>* broadcaster, character&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_character_information_single(::kaminari::broadcaster<B>* broadcaster, character&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_character_information_single(::kaminari::broadcaster<B>* broadcaster, character&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_character_information_single(::kaminari::broadcaster<B>* broadcaster, character&& data);
    template <typename B, typename D>
    void broadcast_character_information_single(::kaminari::broadcaster<B>* broadcaster, character&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_login_character_result(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status_ex&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_login_character_result(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status_ex&& data);
    template <typename B, typename T>
    void broadcast_login_character_result(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_login_character_result(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_login_character_result(::kaminari::broadcaster<B>* broadcaster, status_ex&& data);
    template <typename B, typename D>
    void broadcast_login_character_result(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_login_character_result_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_login_character_result_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_login_character_result_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data);
    template <typename B, typename D>
    void broadcast_login_character_result_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_enter_world(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, success&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_enter_world(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, success&& data);
    template <typename B, typename T>
    void broadcast_enter_world(::kaminari::broadcaster<B>* broadcaster, success&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_enter_world(::kaminari::broadcaster<B>* broadcaster, success&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_enter_world(::kaminari::broadcaster<B>* broadcaster, success&& data);
    template <typename B, typename D>
    void broadcast_enter_world(::kaminari::broadcaster<B>* broadcaster, success&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_enter_world_single(::kaminari::broadcaster<B>* broadcaster, success&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_enter_world_single(::kaminari::broadcaster<B>* broadcaster, success&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_enter_world_single(::kaminari::broadcaster<B>* broadcaster, success&& data);
    template <typename B, typename D>
    void broadcast_enter_world_single(::kaminari::broadcaster<B>* broadcaster, success&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_do_sth(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, complex&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_do_sth(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, complex&& data);
    template <typename B, typename T>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data);
    template <typename B, typename D>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_do_sth_single(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_do_sth_single(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_do_sth_single(::kaminari::broadcaster<B>* broadcaster, complex&& data);
    template <typename B, typename D>
    void broadcast_do_sth_single(::kaminari::broadcaster<B>* broadcaster, complex&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_spawn(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, spawn_data&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_spawn(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, spawn_data&& data);
    template <typename B, typename T>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data);
    template <typename B, typename D>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_spawn_single(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_spawn_single(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_spawn_single(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data);
    template <typename B, typename D>
    void broadcast_spawn_single(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_selected_character_spawn_data(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_spawn_data&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_selected_character_spawn_data(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_spawn_data&& data);
    template <typename B, typename T>
    void broadcast_selected_character_spawn_data(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_selected_character_spawn_data(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_selected_character_spawn_data(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data);
    template <typename B, typename D>
    void broadcast_selected_character_spawn_data(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_selected_character_spawn_data_single(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_selected_character_spawn_data_single(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_selected_character_spawn_data_single(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data);
    template <typename B, typename D>
    void broadcast_selected_character_spawn_data_single(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_spawned_entity(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, spawn&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_spawned_entity(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, spawn&& data);
    template <typename B, typename T>
    void broadcast_spawned_entity(::kaminari::broadcaster<B>* broadcaster, spawn&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_spawned_entity(::kaminari::broadcaster<B>* broadcaster, spawn&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_spawned_entity(::kaminari::broadcaster<B>* broadcaster, spawn&& data);
    template <typename B, typename D>
    void broadcast_spawned_entity(::kaminari::broadcaster<B>* broadcaster, spawn&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_spawned_entity_single(::kaminari::broadcaster<B>* broadcaster, spawn&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_spawned_entity_single(::kaminari::broadcaster<B>* broadcaster, spawn&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_spawned_entity_single(::kaminari::broadcaster<B>* broadcaster, spawn&& data);
    template <typename B, typename D>
    void broadcast_spawned_entity_single(::kaminari::broadcaster<B>* broadcaster, spawn&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_despawned_entity(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, despawn&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_despawned_entity(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, despawn&& data);
    template <typename B, typename T>
    void broadcast_despawned_entity(::kaminari::broadcaster<B>* broadcaster, despawn&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_despawned_entity(::kaminari::broadcaster<B>* broadcaster, despawn&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_despawned_entity(::kaminari::broadcaster<B>* broadcaster, despawn&& data);
    template <typename B, typename D>
    void broadcast_despawned_entity(::kaminari::broadcaster<B>* broadcaster, despawn&& data, D* ignore);
    template <typename B, typename T>
    void broadcast_despawned_entity_single(::kaminari::broadcaster<B>* broadcaster, despawn&& data, T&& callback);
    template <typename B, typename T, typename D>
    void broadcast_despawned_entity_single(::kaminari::broadcaster<B>* broadcaster, despawn&& data, T&& callback, D* ignore);
    template <typename B>
    void broadcast_despawned_entity_single(::kaminari::broadcaster<B>* broadcaster, despawn&& data);
    template <typename B, typename D>
    void broadcast_despawned_entity_single(::kaminari::broadcaster<B>* broadcaster, despawn&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_world_update(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, entity_update&& data);
    template <typename B>
    void broadcast_world_update(::kaminari::broadcaster<B>* broadcaster, entity_update&& data);
    template <typename B, typename D>
    void broadcast_world_update(::kaminari::broadcaster<B>* broadcaster, entity_update&& data, D* ignore);
    template <typename B>
    void broadcast_world_update_single(::kaminari::broadcaster<B>* broadcaster, entity_update&& data);
    template <typename B, typename D>
    void broadcast_world_update_single(::kaminari::broadcaster<B>* broadcaster, entity_update&& data, D* ignore);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_self_world_update(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, self_update&& data, T&& callback);
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_self_world_update(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, self_update&& data);
    template <typename B>
    void broadcast_self_world_update(::kaminari::broadcaster<B>* broadcaster, self_update&& data);
    template <typename B, typename D>
    void broadcast_self_world_update(::kaminari::broadcaster<B>* broadcaster, self_update&& data, D* ignore);
    template <typename B>
    void broadcast_self_world_update_single(::kaminari::broadcaster<B>* broadcaster, self_update&& data);
    template <typename B, typename D>
    void broadcast_self_world_update_single(::kaminari::broadcaster<B>* broadcaster, self_update&& data, D* ignore);
}

namespace kumo
{
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_character_created(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_selection&& data, T&& callback)
    {
        pq->send_reliable(opcode::character_created, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_character_created(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_selection&& data)
    {
        pq->send_reliable(opcode::character_created, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_character_created(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_created, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_character_created(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_created, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_character_created(::kaminari::broadcaster<B>* broadcaster, character_selection&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_created);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_character_created(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_created);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_character_created_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_created, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_character_created_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_created, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_character_created_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_created);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_character_created_single(::kaminari::broadcaster<B>* broadcaster, character_selection&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_created);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_handshake_response(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status&& data, T&& callback)
    {
        pq->send_reliable(opcode::handshake_response, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_handshake_response(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status&& data)
    {
        pq->send_reliable(opcode::handshake_response, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_handshake_response(::kaminari::broadcaster<B>* broadcaster, status&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::handshake_response, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_handshake_response(::kaminari::broadcaster<B>* broadcaster, status&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::handshake_response, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_handshake_response(::kaminari::broadcaster<B>* broadcaster, status&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::handshake_response);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_handshake_response(::kaminari::broadcaster<B>* broadcaster, status&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::handshake_response);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_handshake_response_single(::kaminari::broadcaster<B>* broadcaster, status&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::handshake_response, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_handshake_response_single(::kaminari::broadcaster<B>* broadcaster, status&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::handshake_response, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_handshake_response_single(::kaminari::broadcaster<B>* broadcaster, status&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::handshake_response);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_handshake_response_single(::kaminari::broadcaster<B>* broadcaster, status&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::handshake_response);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_login_response(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status_ex&& data, T&& callback)
    {
        pq->send_reliable(opcode::login_response, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_login_response(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status_ex&& data)
    {
        pq->send_reliable(opcode::login_response, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_login_response(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_response, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_login_response(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_response, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_login_response(::kaminari::broadcaster<B>* broadcaster, status_ex&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_response);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_login_response(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_response);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_login_response_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_response, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_login_response_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_response, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_login_response_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_response);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_login_response_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_response);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_characters_list(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, characters_list_data&& data, T&& callback)
    {
        pq->send_reliable(opcode::characters_list, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_characters_list(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, characters_list_data&& data)
    {
        pq->send_reliable(opcode::characters_list, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_characters_list(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::characters_list, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_characters_list(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::characters_list, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_characters_list(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::characters_list);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_characters_list(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::characters_list);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_characters_list_single(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::characters_list, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_characters_list_single(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::characters_list, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_characters_list_single(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::characters_list);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_characters_list_single(::kaminari::broadcaster<B>* broadcaster, characters_list_data&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::characters_list);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_character_information(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character&& data, T&& callback)
    {
        pq->send_reliable(opcode::character_information, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_character_information(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character&& data)
    {
        pq->send_reliable(opcode::character_information, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_character_information(::kaminari::broadcaster<B>* broadcaster, character&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_information, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_character_information(::kaminari::broadcaster<B>* broadcaster, character&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_information, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_character_information(::kaminari::broadcaster<B>* broadcaster, character&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_information);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_character_information(::kaminari::broadcaster<B>* broadcaster, character&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_information);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_character_information_single(::kaminari::broadcaster<B>* broadcaster, character&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_information, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_character_information_single(::kaminari::broadcaster<B>* broadcaster, character&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_information, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_character_information_single(::kaminari::broadcaster<B>* broadcaster, character&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_information);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_character_information_single(::kaminari::broadcaster<B>* broadcaster, character&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::character_information);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_login_character_result(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status_ex&& data, T&& callback)
    {
        pq->send_reliable(opcode::login_character_result, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_login_character_result(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, status_ex&& data)
    {
        pq->send_reliable(opcode::login_character_result, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_login_character_result(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_character_result, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_login_character_result(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_character_result, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_login_character_result(::kaminari::broadcaster<B>* broadcaster, status_ex&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_character_result);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_login_character_result(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_character_result);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_login_character_result_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_character_result, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_login_character_result_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_character_result, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_login_character_result_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_character_result);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_login_character_result_single(::kaminari::broadcaster<B>* broadcaster, status_ex&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::login_character_result);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_enter_world(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, success&& data, T&& callback)
    {
        pq->send_reliable(opcode::enter_world, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_enter_world(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, success&& data)
    {
        pq->send_reliable(opcode::enter_world, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_enter_world(::kaminari::broadcaster<B>* broadcaster, success&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::enter_world, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_enter_world(::kaminari::broadcaster<B>* broadcaster, success&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::enter_world, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_enter_world(::kaminari::broadcaster<B>* broadcaster, success&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::enter_world);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_enter_world(::kaminari::broadcaster<B>* broadcaster, success&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::enter_world);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_enter_world_single(::kaminari::broadcaster<B>* broadcaster, success&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::enter_world, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_enter_world_single(::kaminari::broadcaster<B>* broadcaster, success&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::enter_world, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_enter_world_single(::kaminari::broadcaster<B>* broadcaster, success&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::enter_world);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_enter_world_single(::kaminari::broadcaster<B>* broadcaster, success&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::enter_world);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_do_sth(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, complex&& data, T&& callback)
    {
        pq->send_reliable(opcode::do_sth, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_do_sth(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, complex&& data)
    {
        pq->send_reliable(opcode::do_sth, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::do_sth, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::do_sth, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::do_sth);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_do_sth(::kaminari::broadcaster<B>* broadcaster, complex&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::do_sth);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_do_sth_single(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::do_sth, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_do_sth_single(::kaminari::broadcaster<B>* broadcaster, complex&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::do_sth, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_do_sth_single(::kaminari::broadcaster<B>* broadcaster, complex&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::do_sth);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_do_sth_single(::kaminari::broadcaster<B>* broadcaster, complex&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::do_sth);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_spawn(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, spawn_data&& data, T&& callback)
    {
        pq->send_reliable(opcode::spawn, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_spawn(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, spawn_data&& data)
    {
        pq->send_reliable(opcode::spawn, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawn, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawn, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawn);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_spawn(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawn);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_spawn_single(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawn, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_spawn_single(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawn, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_spawn_single(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawn);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_spawn_single(::kaminari::broadcaster<B>* broadcaster, spawn_data&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawn);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_selected_character_spawn_data(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_spawn_data&& data, T&& callback)
    {
        pq->send_reliable(opcode::selected_character_spawn_data, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_selected_character_spawn_data(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, character_spawn_data&& data)
    {
        pq->send_reliable(opcode::selected_character_spawn_data, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_selected_character_spawn_data(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::selected_character_spawn_data, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_selected_character_spawn_data(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::selected_character_spawn_data, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_selected_character_spawn_data(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::selected_character_spawn_data);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_selected_character_spawn_data(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::selected_character_spawn_data);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_selected_character_spawn_data_single(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::selected_character_spawn_data, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_selected_character_spawn_data_single(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::selected_character_spawn_data, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <typename B>
    void broadcast_selected_character_spawn_data_single(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::selected_character_spawn_data);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_reliable(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_selected_character_spawn_data_single(::kaminari::broadcaster<B>* broadcaster, character_spawn_data&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::selected_character_spawn_data);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_reliable(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_spawned_entity(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, spawn&& data, T&& callback)
    {
        pq->send_ordered(opcode::spawned_entity, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_spawned_entity(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, spawn&& data)
    {
        pq->send_ordered(opcode::spawned_entity, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_spawned_entity(::kaminari::broadcaster<B>* broadcaster, spawn&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawned_entity, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_spawned_entity(::kaminari::broadcaster<B>* broadcaster, spawn&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawned_entity, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_ordered(packet);
            }
        });
    }
    template <typename B>
    void broadcast_spawned_entity(::kaminari::broadcaster<B>* broadcaster, spawn&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawned_entity);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_spawned_entity(::kaminari::broadcaster<B>* broadcaster, spawn&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawned_entity);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_ordered(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_spawned_entity_single(::kaminari::broadcaster<B>* broadcaster, spawn&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawned_entity, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_spawned_entity_single(::kaminari::broadcaster<B>* broadcaster, spawn&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawned_entity, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_ordered(packet);
            }
        });
    }
    template <typename B>
    void broadcast_spawned_entity_single(::kaminari::broadcaster<B>* broadcaster, spawn&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawned_entity);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_spawned_entity_single(::kaminari::broadcaster<B>* broadcaster, spawn&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::spawned_entity);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_ordered(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_despawned_entity(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, despawn&& data, T&& callback)
    {
        pq->send_ordered(opcode::despawned_entity, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_despawned_entity(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, despawn&& data)
    {
        pq->send_ordered(opcode::despawned_entity, std::move(data));
    }
    template <typename B, typename T>
    void broadcast_despawned_entity(::kaminari::broadcaster<B>* broadcaster, despawn&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::despawned_entity, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_despawned_entity(::kaminari::broadcaster<B>* broadcaster, despawn&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::despawned_entity, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_ordered(packet);
            }
        });
    }
    template <typename B>
    void broadcast_despawned_entity(::kaminari::broadcaster<B>* broadcaster, despawn&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::despawned_entity);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_despawned_entity(::kaminari::broadcaster<B>* broadcaster, despawn&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::despawned_entity);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_ordered(packet);
            }
        });
    }
    template <typename B, typename T>
    void broadcast_despawned_entity_single(::kaminari::broadcaster<B>* broadcaster, despawn&& data, T&& callback)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::despawned_entity, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename T, typename D>
    void broadcast_despawned_entity_single(::kaminari::broadcaster<B>* broadcaster, despawn&& data, T&& callback, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::despawned_entity, std::forward<T>(callback));
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_ordered(packet);
            }
        });
    }
    template <typename B>
    void broadcast_despawned_entity_single(::kaminari::broadcaster<B>* broadcaster, despawn&& data)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::despawned_entity);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet](auto pq) {
            pq->send_ordered(packet);
        });
    }
    template <typename B, typename D>
    void broadcast_despawned_entity_single(::kaminari::broadcaster<B>* broadcaster, despawn&& data, D* ignore)
    {
        boost::intrusive_ptr<::kaminari::buffers::packet> packet = ::kaminari::buffers::packet::make((uint16_t)opcode::despawned_entity);
        ::kumo::marshal::pack(packet, data);
        broadcaster->broadcast_single([packet, ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_ordered(packet);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_world_update(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, entity_update&& data)
    {
        pq->send_eventually_synced(opcode::world_update, std::move(data));
    }
    template <typename B>
    void broadcast_world_update(::kaminari::broadcaster<B>* broadcaster, entity_update&& data)
    {
        broadcaster->broadcast([data = std::move(data)](auto pq) {
            pq->send_eventually_synced(opcode::world_update, data);
        });
    }
    template <typename B, typename D>
    void broadcast_world_update(::kaminari::broadcaster<B>* broadcaster, entity_update&& data, D* ignore)
    {
        broadcaster->broadcast([data = std::move(data), ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_eventually_synced(opcode::world_update, data);
            }
        });
    }
    template <typename B>
    void broadcast_world_update_single(::kaminari::broadcaster<B>* broadcaster, entity_update&& data)
    {
        broadcaster->broadcast_single([data = std::move(data)](auto pq) {
            pq->send_eventually_synced(opcode::world_update, data);
        });
    }
    template <typename B, typename D>
    void broadcast_world_update_single(::kaminari::broadcaster<B>* broadcaster, entity_update&& data, D* ignore)
    {
        broadcaster->broadcast_single([data = std::move(data), ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_eventually_synced(opcode::world_update, data);
            }
        });
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator, typename T>
    inline void send_self_world_update(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, self_update&& data, T&& callback)
    {
        pq->send_most_recent(opcode::self_world_update, std::move(data), std::forward<T>(callback));
    }
    template <class ReliableAllocator, class Most_recentAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    inline void send_self_world_update(::kumo::protocol_queues<ReliableAllocator, Most_recentAllocator, OrderedAllocator, Eventually_syncedAllocator>* pq, self_update&& data)
    {
        pq->send_most_recent(opcode::self_world_update, std::move(data));
    }
    template <typename B>
    void broadcast_self_world_update(::kaminari::broadcaster<B>* broadcaster, self_update&& data)
    {
        broadcaster->broadcast([data = std::move(data)](auto pq) {
            pq->send_most_recent(opcode::self_world_update, data);
        });
    }
    template <typename B, typename D>
    void broadcast_self_world_update(::kaminari::broadcaster<B>* broadcaster, self_update&& data, D* ignore)
    {
        broadcaster->broadcast([data = std::move(data), ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_most_recent(opcode::self_world_update, data);
            }
        });
    }
    template <typename B>
    void broadcast_self_world_update_single(::kaminari::broadcaster<B>* broadcaster, self_update&& data)
    {
        broadcaster->broadcast_single([data = std::move(data)](auto pq) {
            pq->send_most_recent(opcode::self_world_update, data);
        });
    }
    template <typename B, typename D>
    void broadcast_self_world_update_single(::kaminari::broadcaster<B>* broadcaster, self_update&& data, D* ignore)
    {
        broadcaster->broadcast_single([data = std::move(data), ignore](auto pq) {
            if (pq != ignore)
            {
                pq->send_most_recent(opcode::self_world_update, data);
            }
        });
    }
}
