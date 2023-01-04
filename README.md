# SynthPy
Synth for Pi Pico written in Circuitpython

```math
 i = \begin{bmatrix}  0 & 1 & 2 & ... n
 \end{bmatrix}
 ```
```math
 freq_coefficients = \begin{bmatrix}  f_0 \\  
                  f_1 \\  
                  ...\\
                  f_n
 \end{bmatrix}
 ```
 
 ```math
 ampl_coefficients = \begin{bmatrix}  a_0 \\  
                  a_1 \\  
                  ...\\
                  a_n
 \end{bmatrix}
```

```math
 signal_{matrix} = freq_coefficients \cdot i  = \begin{bmatrix}  f_0 \\  
                  f_1 \\  
                  ...\\
                  a_n
 \end{bmatrix} 
 \cdot
 \begin{bmatrix}  0 & 1 & 2 & ... n
 
 \end{bmatrix} 
 \cdot \frac{f2\pi}{sample\_rate} 
 = \begin{bmatrix}  f_0*0 & f_0*1 & f_0*2 &... & f_0*n\\  
                  f_1*0 & f_1*1 & f_1*2 &... & f_0*n\\  
                  ...\\
                  f_n*0 & f_n*1 & f_n*2 &... & f_n*n\\  
 \end{bmatrix} \cdot \frac{f2\pi}{sample\_rate} 
```


```math 
signal_{matrix} = 
\begin{bmatrix}  \frac{0f_0f2\pi}{sample\_rate} & \frac{1f_0f2\pi}{sample\_rate} & \frac{2f_0f2\pi}{sample\_rate}& ... & & \frac{nf_0f2\pi}{sample\_rate}\\  
                  \frac{0f_1f2\pi}{sample\_rate} & \frac{1f_1f2\pi}{sample\_rate} & \frac{2f_1f2\pi}{sample\_rate}& ... & & \frac{nf_1f2\pi}{sample\_rate}\\  
                  ...\\
                  \frac{0f_nf2\pi}{sample\_rate} & \frac{1f_nf2\pi}{sample\_rate} & \frac{2f_nf2\pi}{sample\_rate}& ... & & \frac{nf_nf2\pi}{sample\_rate}\\  
 \end{bmatrix}
  \cdot \frac{f2\pi}{sample\_rate} 
```


```math 
signal = flatten(signal_{matrix})= 
\begin{bmatrix}   \frac{nf_0f2\pi}{sample\_rate}
                  ...
                  \frac{nf_1f2\pi}{sample\_rate}
                  ...
                   \frac{nf_nf2\pi}{sample\_rate}  
 \end{bmatrix}
```

```math
fourier\_series_{matrix} = sin(signal) \cdot ampl_coefficients = sin(
\begin{bmatrix}   \frac{nf_0f2\pi}{sample\_rate}
                  ...
                  \frac{nf_1f2\pi}{sample\_rate}
                  ...
                   \frac{nf_nf2\pi}{sample\_rate}  
 \end{bmatrix})
 \cdot
 \begin{bmatrix}  a_0 \\  
                  a_1 \\  
                  ...\\
                  a_n
 \end{bmatrix}
 
 
```
```math
fourier\_series_{matrix} = 

 \begin{bmatrix}  a_0sin(\frac{0f_0f2\pi}{sample\_rate}) & \frac{1f_0f2\pi}{sample\_rate} & \frac{2f_0f2\pi}{sample\_rate}& ... & & \frac{nf_0f2\pi}{sample\_rate}\\  
                  \frac{0f_1f2\pi}{sample\_rate} & \frac{1f_1f2\pi}{sample\_rate} & \frac{2f_1f2\pi}{sample\_rate}& ... & & \frac{nf_1f2\pi}{sample\_rate}\\  
                  ...\\
                  \frac{0f_nf2\pi}{sample\_rate} & \frac{1f_nf2\pi}{sample\_rate} & \frac{2f_nf2\pi}{sample\_rate}& ... & & \frac{nf_nf2\pi}{sample\_rate}\\  
 \end{bmatrix}
```


![Image of various signals](https://github.com/MartinTykhelle/SynthPy/blob/main/synth.py.png?raw=true)

