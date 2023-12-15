( 
 SynthDef('from_blender', {
var impulse_freq = 0.5, impulse_phase = 0.0, impulse_mul = 1.0, impulse_add = 0.0;
var impulse = Impulse.kr(impulse_freq, impulse_phase, impulse_mul, impulse_add);
var envelope_gate = impulse, envelope_attack = 0.0, envelope_decay = 0.0, envelope_sustain = 0.0, envelope_release = 2.0;
var envelope = EnvGen.kr(Env.adsr(envelope_attack, envelope_decay, envelope_sustain, envelope_release), envelope_gate, doneAction:2);
var saw_freq = 440.0, saw_mul = envelope, saw_add = 0.0;
var saw = Saw.ar(saw_freq, saw_mul, saw_add);

 Out.ar(0, saw)
}).add
)
 
Synth('from_blender')