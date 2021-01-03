#pragma once
#include <inttypes.h>
#include <map>
#include <boost/intrusive_ptr.hpp>
#include <kumo/opcodes.hpp>
#include <kumo/marshal.hpp>
#include <kaminari/queues/reliable_queue.hpp>
#include <kaminari/queues/unreliable_queue.hpp>
#include <kaminari/queues/eventually_synced_queue.hpp>
#include <kaminari/packers/immediate_packer.hpp>
#include <kaminari/packers/merge_packer.hpp>
#include <kaminari/packers/most_recent_packer_by_opcode.hpp>
#include <kaminari/packers/ordered_packer.hpp>
#include <kaminari/packers/unique_merge_packer.hpp>
namespace kaminari
{
    class packet;
}
namespace kaminari
{
    namespace detail
    {
        using packets_by_block = std::map<uint32_t, std::vector<boost::intrusive_ptr<packet>>>;
    }
}
namespace kumo
{
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    class protocol_queues;
}

namespace kumo
{
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    class protocol_queues
    {
    public:
        template <typename... Args>
         protocol_queues(uint8_t resend_threshold, Args&&... allocator_args);
        void reset();
        void ack(uint16_t block_id);
        void process(uint16_t block_id, uint16_t& remaining, typename ::kaminari::detail::packets_by_block& by_block);
        template <typename D, typename T>
        void send_unreliable(::kumo::opcode opcode, D&& data, T&& callback);
        template <typename D>
        void send_unreliable(::kumo::opcode opcode, D&& data);
        void send_unreliable(const boost::intrusive_ptr<::kaminari::packet>& packet);
        template <typename D, typename T>
        void send_reliable(::kumo::opcode opcode, D&& data, T&& callback);
        template <typename D>
        void send_reliable(::kumo::opcode opcode, D&& data);
        void send_reliable(const boost::intrusive_ptr<::kaminari::packet>& packet);
        template <typename D, typename T>
        void send_ordered(::kumo::opcode opcode, D&& data, T&& callback);
        template <typename D>
        void send_ordered(::kumo::opcode opcode, D&& data);
        void send_ordered(const boost::intrusive_ptr<::kaminari::packet>& packet);
        template <typename D>
        void send_eventually_synced(::kumo::opcode opcode, D&& data);
    private:
        ::kaminari::unreliable_queue<::kaminari::immediate_packer<::kumo::marshal, UnreliableAllocator>> _unreliable;
        ::kaminari::reliable_queue<::kaminari::immediate_packer<::kumo::marshal, ReliableAllocator>> _reliable;
        ::kaminari::reliable_queue<::kaminari::ordered_packer<::kumo::marshal, OrderedAllocator>> _ordered;
        ::kaminari::eventually_synced_queue<::kaminari::unique_merge_packer<world_update_data, entity_update, ::kumo::opcode::world_update, ::kumo::marshal, Eventually_syncedAllocator>> _eventually_synced;
    };

    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    template <typename... Args>
     protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::protocol_queues(uint8_t resend_threshold, Args&&... allocator_args):
        _unreliable(resend_threshold, std::get<0>(std::forward_as_tuple(allocator_args...))),
        _reliable(resend_threshold, std::get<1>(std::forward_as_tuple(allocator_args...))),
        _ordered(resend_threshold, std::get<2>(std::forward_as_tuple(allocator_args...))),
        _eventually_synced(resend_threshold, std::get<3>(std::forward_as_tuple(allocator_args...)))
    {
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::reset()
    {
        _unreliable.reset();
        _reliable.reset();
        _ordered.reset();
        _eventually_synced.reset();
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::ack(uint16_t block_id)
    {
        _unreliable.ack(block_id);
        _reliable.ack(block_id);
        _ordered.ack(block_id);
        _eventually_synced.ack(block_id);
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::process(uint16_t block_id, uint16_t& remaining, typename ::kaminari::detail::packets_by_block& by_block)
    {
        _unreliable.process(block_id, remaining, by_block);
        _reliable.process(block_id, remaining, by_block);
        _ordered.process(block_id, remaining, by_block);
        _eventually_synced.process(block_id, remaining, by_block);
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    template <typename D, typename T>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_unreliable(::kumo::opcode opcode, D&& data, T&& callback)
    {
        _unreliable.add(static_cast<uint16_t>(opcode), std::forward<D>(data), std::forward<T>(callback));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    template <typename D>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_unreliable(::kumo::opcode opcode, D&& data)
    {
        _unreliable.add(static_cast<uint16_t>(opcode), std::forward<D>(data));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_unreliable(const boost::intrusive_ptr<::kaminari::packet>& packet)
    {
        _unreliable.add(packet);
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    template <typename D, typename T>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_reliable(::kumo::opcode opcode, D&& data, T&& callback)
    {
        _reliable.add(static_cast<uint16_t>(opcode), std::forward<D>(data), std::forward<T>(callback));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    template <typename D>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_reliable(::kumo::opcode opcode, D&& data)
    {
        _reliable.add(static_cast<uint16_t>(opcode), std::forward<D>(data));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_reliable(const boost::intrusive_ptr<::kaminari::packet>& packet)
    {
        _reliable.add(packet);
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    template <typename D, typename T>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_ordered(::kumo::opcode opcode, D&& data, T&& callback)
    {
        _ordered.add(static_cast<uint16_t>(opcode), std::forward<D>(data), std::forward<T>(callback));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    template <typename D>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_ordered(::kumo::opcode opcode, D&& data)
    {
        _ordered.add(static_cast<uint16_t>(opcode), std::forward<D>(data));
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_ordered(const boost::intrusive_ptr<::kaminari::packet>& packet)
    {
        _ordered.add(packet);
    }
    template <class UnreliableAllocator, class ReliableAllocator, class OrderedAllocator, class Eventually_syncedAllocator>
    template <typename D>
    void protocol_queues<UnreliableAllocator, ReliableAllocator, OrderedAllocator, Eventually_syncedAllocator>::send_eventually_synced(::kumo::opcode opcode, D&& data)
    {
        _eventually_synced.add(static_cast<uint16_t>(opcode), std::forward<D>(data));
    }
}
