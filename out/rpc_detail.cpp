#include <kumo/rpc_detail.hpp>
namespace kumo
{
    namespace detail
    {
        void send_reliable(client* client, const ::kaminari::packet::ptr& packet)
        {
            client->send_reliable(packet);
        }
        void send_ordered(client* client, const ::kaminari::packet::ptr& packet)
        {
            client->send_ordered(packet);
        }
    }
}
