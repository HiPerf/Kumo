#include <boost/intrusive_ptr.hpp>
class client;
namespace kaminari
{
    class packet
    {
        public:
        using ptr = boost::intrusive_ptr<packet>;
    };
}
namespace kumo
{
    namespace detail
    {
        void send_reliable(client* client, const ::kaminari::packet::ptr& packet);
        void send_ordered(client* client, const ::kaminari::packet::ptr& packet);
    }
}

namespace kumo
{
    namespace detail
    {
    }
}
