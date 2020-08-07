#include <kumo/protocol_queues.hpp>
namespace kumo
{
    void protocol_queues::reset()
    {
        _reliable.reset();
        _ordered.reset();
    }
    void protocol_queues::ack(uint16_t block_id)
    {
        _reliable.ack(block_id);
        _ordered.ack(block_id);
    }
    void protocol_queues::process(uint16_t id, uint16_t& remaining, typename ::kumo::detail::packets_by_block& by_block)
    {
        _reliable.process(block_id, remaining, by_block);
        _ordered.process(block_id, remaining, by_block);
    }
    void protocol_queues::send_reliable(const boost::intrusive_ptr<::kaminari::packet>& packet)
    {
        _reliable.add(packet);
    }
    void protocol_queues::send_ordered(const boost::intrusive_ptr<::kaminari::packet>& packet)
    {
        _ordered.add(packet);
    }
}
