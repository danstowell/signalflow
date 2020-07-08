#pragma once

#include "signal/buffer/buffer.h"
#include "signal/buffer/buffer2D.h"
#include "signal/node/node.h"

namespace libsignal
{
class Wavetable : public Node
{
public:
    Wavetable(BufferRef buffer = nullptr,
              NodeRef frequency = 440,
              NodeRef sync = 0);

    virtual void process(sample **out, int num_frames);

private:
    BufferRef buffer;
    NodeRef frequency;
    NodeRef sync;
    float phase[SIGNAL_MAX_CHANNELS];
};

class Wavetable2D : public Node
{
public:
    Wavetable2D(BufferRef2D buffer = nullptr,
                NodeRef frequency = 440,
                NodeRef crossfade = 0.0,
                NodeRef sync = 0);

    virtual void process(sample **out, int num_frames);

private:
    BufferRef2D buffer;
    NodeRef frequency;
    NodeRef crossfade;
    NodeRef sync;
    float phase[SIGNAL_MAX_CHANNELS];
};

REGISTER(Wavetable, "wavetable")
REGISTER(Wavetable2D, "wavetable2d")
}
