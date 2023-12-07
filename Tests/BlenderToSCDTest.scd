( 
 SynthDef('from_blender', {
var impulse_freq = 440.0, impulse_phase = 0.0, impulse_mul = 1.0, impulse_add = 0.0;
var impulse = Pulse.ar(impulse_freq, impulse_phase, impulse_mul, impulse_add);
var envelope_gate = impulse, envelope_attack = 0.019999999552965164, envelope_decay = 0.5, envelope_sustain = 1.0, envelope_release = 1.0;
var envelope = EnvGen.kr(Env.adsr(envelope_attack, envelope_decay, envelope_sustain, envelope_release), envelope_gate, doneAction:2);
var pulse_freq = 400.0, pulse_width = 0.0, pulse_mul = 5.0, pulse_add = envelope;
var pulse = Pulse.ar(pulse_freq, pulse_width, pulse_mul, pulse_add);
var lowpassfilter_input = pulse, lowpassfilter_frequency = 2000.0, lowpassfilter_mul = 1.0, lowpassfilter_add = 0.0;
var lowpassfilter = LPF.ar(lowpassfilter_input, lowpassfilter_frequency, lowpassfilter_mul, lowpassfilter_add);

 Out.ar(0, lowpassfilter)
}).add
)
 
Synth('from_blender')