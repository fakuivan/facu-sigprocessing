import IPython.display
import numpy as np
import json

# Gets around a limitation in vscode that will not allow us to play regular audio,
# since audio codecs are removed from electron to reduce package size. This is
# apparently already solved in the insider builds
## https://github.com/microsoft/vscode/issues/118275#issuecomment-1173073070
# Taken from:
## https://github.com/microsoft/vscode-jupyter/issues/1012#issuecomment-785410064
def Audio(audio: np.ndarray, sr: int):
    """
    Use instead of IPython.display.Audio as a workaround for VS Code.
    `audio` is an array with shape (channels, samples) or just (samples,) for mono.
    """

    if np.ndim(audio) == 1:
        channels = [audio.tolist()]
    else:
        channels = audio.tolist()

    return IPython.display.HTML("""
        <script>
            if (!window.audioContext) {
                window.audioContext = new AudioContext();
                window.source = undefined;
                window.playAudio = function(audioChannels, sr) {
                    const buffer = audioContext.createBuffer(audioChannels.length, audioChannels[0].length, sr);
                    for (let [channel, data] of audioChannels.entries()) {
                        buffer.copyToChannel(Float32Array.from(data), channel);
                    }
            
                    const source = audioContext.createBufferSource();
                    window.source = source;
                    source.buffer = buffer;
                    source.connect(audioContext.destination);
                    source.start();
                };
                window.stopAudio = function() {
                    if (window.source) {
                        window.source.stop();
                    }
                }
            }
        </script>
        <div>
            <button onclick="window.playAudio(%s, %s)">Play</button>
            <button onclick="window.stopAudio()">Stop</button>
        </div>
    """ % (json.dumps(channels), sr))

def mono(xss):
    channels = xss.shape[1]
    return xss.sum(axis=1) / channels

def init_sp_printing(sp = None):
    if sp is None:
        import sympy as sp
    
    from matplotlib import MatplotlibDeprecationWarning
    import warnings
    warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)

    return sp.init_printing()