#include <optional>
#include <vector>
#include <inttypes.h>
namespace kumo
{
    struct complex
    {
    public:
        std::optional<uint32_t> x;
        std::vector<spawn_data> y;
        int32_t z;
        std::optional<std::vector<bool>> w;
    };

    struct has_id
    {
    public:
        int64_t id;
    };

    struct spawn_data : public has_id 
    {
    public:
        int8_t x;
        int8_t y;
    };

    struct movement
    {
    public:
        int8_t direction;
    };

}

namespace kumo
{
}
