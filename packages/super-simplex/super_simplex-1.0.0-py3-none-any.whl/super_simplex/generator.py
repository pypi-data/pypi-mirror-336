from .dimensions.two import *
from .dimensions.three import *
from .dimensions.four import *

from .l_math import *

from .l_random import *


class Gener():
    def __init__(self, seeds : list[int]):
        self.seeds = seeds

        temp = [gen_permu(seed) for seed in self.seeds]

        self.perms, self.perms_grad_index3 = zip(*temp)

    def noise_2d(self, x : float, y : float, octaves : int = 1, initial_amplitude : float = 1.0, initial_frequency : float = 1.0, persistence : float = 1.0, lacunarity : float = 1.0, octave_offset_scale : float = 1.0) -> list[float]:
        values = []

        for index in range(len(self.seeds)):
            amplitude = initial_amplitude
            frequency = initial_frequency
            total = 0.0
            max_amplitude = 0.0
            
            for _ in range(octaves):
                offset = random_1f2(_, self.seeds[index])
                total += amplitude * noise_2d(x * frequency + offset[0] * octave_offset_scale, y * frequency + offset[1] * octave_offset_scale, self.perms[index])
                max_amplitude += amplitude
                amplitude *= persistence
                frequency *= lacunarity
                
            values.append(total / max_amplitude)

        return values
    
    def noise_2d_array(self, x : np.ndarray, y : np.ndarray, octaves : int = 1, initial_amplitude : float = 1.0, initial_frequency : float = 1.0, persistence : float = 1.0, lacunarity : float = 1.0, octave_offset_scale : float = 1.0) -> list[np.ndarray]:
        arrays = []

        for index in range(len(self.seeds)):
            amplitude = initial_amplitude
            frequency = initial_frequency
            total = np.zeros((y.size, x.size))
            max_amplitude = 0.0
            
            for _ in range(octaves):
                offset = random_1f2(_, self.seeds[index])
                total += amplitude * noise_2d_array(x * frequency + offset[0] * octave_offset_scale, y * frequency + offset[1] * octave_offset_scale, self.perms[index])
                max_amplitude += amplitude
                amplitude *= persistence
                frequency *= lacunarity
                
            arrays.append(total / max_amplitude)

        return arrays
    
    def noise_3d(self, x : float, y : float, z : float, octaves : int = 1, initial_amplitude : float = 1.0, initial_frequency : float = 1.0, persistence : float = 1.0, lacunarity : float = 1.0, octave_offset_scale : float = 1.0) -> list[float]:
        values = []

        for index in range(len(self.seeds)):
            amplitude = initial_amplitude
            frequency = initial_frequency
            total = 0.0
            max_amplitude = 0.0
            
            for _ in range(octaves):
                offset = random_1f3(_, self.seeds[index])
                total += amplitude * noise_3d(x * frequency + offset[0] * octave_offset_scale, y * frequency + offset[1] * octave_offset_scale, z * frequency + offset[2] * octave_offset_scale, self.perms[index], self.perms_grad_index3[index])
                max_amplitude += amplitude
                amplitude *= persistence
                frequency *= lacunarity
                
            values.append(total / max_amplitude)

        return values
    
    def noise_3d_array(self, x : np.ndarray, y : np.ndarray, z : np.ndarray, octaves : int = 1, initial_amplitude : float = 1.0, initial_frequency : float = 1.0, persistence : float = 1.0, lacunarity : float = 1.0, octave_offset_scale : float = 1.0) -> list[np.ndarray]:
        arrays = []

        for index in range(len(self.seeds)):
            amplitude = initial_amplitude
            frequency = initial_frequency
            total = np.zeros((z.size, y.size, x.size))
            max_amplitude = 0.0
            
            for _ in range(octaves):
                offset = random_1f3(_, self.seeds[index])
                total += amplitude * noise_3d_array(x * frequency + offset[0] * octave_offset_scale, y * frequency + offset[1] * octave_offset_scale, z * frequency + offset[2] * octave_offset_scale, self.perms[index], self.perms_grad_index3[index])
                max_amplitude += amplitude
                amplitude *= persistence
                frequency *= lacunarity
                
            arrays.append(total / max_amplitude)

        return arrays
    
    def noise_4d(self, x : float, y : float, z : float, w : float, octaves : int = 1, initial_amplitude : float = 1.0, initial_frequency : float = 1.0, persistence : float = 1.0, lacunarity : float = 1.0, octave_offset_scale : float = 1.0) -> list[float]:
        values = []

        for index in range(len(self.seeds)):
            amplitude = initial_amplitude
            frequency = initial_frequency
            total = 0.0
            max_amplitude = 0.0
            
            for _ in range(octaves):
                offset = random_1f4(_, self.seeds[index])
                total += amplitude * noise_4d(x * frequency + offset[0] * octave_offset_scale, y * frequency + offset[1] * octave_offset_scale, z * frequency + offset[2] * octave_offset_scale, w * frequency + offset[3] * octave_offset_scale, self.perms[index])
                max_amplitude += amplitude
                amplitude *= persistence
                frequency *= lacunarity
                
            values.append(total / max_amplitude)

        return values
    
    def noise_4d_array(self, x : np.ndarray, y : np.ndarray, z : np.ndarray, w : np.ndarray, octaves : int = 1, initial_amplitude : float = 1.0, initial_frequency : float = 1.0, persistence : float = 1.0, lacunarity : float = 1.0, octave_offset_scale : float = 1.0) -> list[np.ndarray]:
        arrays = []

        for index in range(len(self.seeds)):
            amplitude = initial_amplitude
            frequency = initial_frequency
            total = np.zeros((w.size, z.size, y.size, x.size))
            max_amplitude = 0.0
            
            for _ in range(octaves):
                offset = random_1f4(_, self.seeds[index])
                total += amplitude * noise_4d_array(x * frequency + offset[0] * octave_offset_scale, y * frequency + offset[1] * octave_offset_scale, z * frequency + offset[2] * octave_offset_scale, w * frequency + offset[3] * octave_offset_scale, self.perms[index])
                max_amplitude += amplitude
                amplitude *= persistence
                frequency *= lacunarity
                
            arrays.append(total / max_amplitude)

        return arrays