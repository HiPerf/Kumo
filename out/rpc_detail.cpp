namespace kaminari
{
    namespace detail
    {
        void send_reliable(client* client, const packet::ptr& packet)
        {
            client->send_reliable(packet);
        }
        void send_ordered(client* client, const packet::ptr& packet)
        {
            client->send_ordered(packet);
        }
    }
}
