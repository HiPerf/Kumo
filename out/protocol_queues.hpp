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
    class protocol_queues;
}

namespace kumo
{
    class protocol_queues
    {
    public:
        template <typename... Args>
         protocol_queues(uint8_t resend_threshold, Args&&... allocator_args);
        void reset();
        void ack(uint16_t block_id);
        void process(uint16_t id, uint16_t& remaining, typename ::kaminari::detail::packets_by_block& by_block);
        template <typename D, typename T>
        void send_reliable(::kumo::opcode opcode, D&& data, T&& callback);
        void send_reliable(const boost::intrusive_ptr<::kaminari::packet>& packet);
        template <typename D, typename T>
        void send_ordered(::kumo::opcode opcode, D&& data, T&& callback);
        void send_ordered(const boost::intrusive_ptr<::kaminari::packet>& packet);
    private:
        ::kaminari::reliable_queue<::kaminari::immediate_packer<::kumo::marshal>> _reliable;
        ::kaminari::reliable_queue<::kaminari::ordered_packer<::kumo::marshal>> _ordered;
    };

    template <typename... Args>
     protocol_queues::protocol_queues(uint8_t resend_threshold, Args&&... allocator_args):
        _reliable(resend_threshold, std::forward<Args>(allocator_args)...),
        _ordered(resend_threshold, std::forward<Args>(allocator_args)...)
    {
    }
    template <typename D, typename T>
    void protocol_queues::send_reliable(::kumo::opcode opcode, D&& data, T&& callback)
    {
        _reliable.add(opcode, std::forward<D>(data), std::forward<T>(callback));
    }
    template <typename D, typename T>
    void protocol_queues::send_ordered(::kumo::opcode opcode, D&& data, T&& callback)
    {
        _ordered.add(opcode, std::forward<D>(data), std::forward<T>(callback));
    }
}
