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
 signal_{matrix} = \frac{f2\pi}{sample\_rate} freq\_coefficients \cdot i  = 
 \frac{f2\pi}{sample\_rate} 
 \begin{bmatrix}  f_0 \\  
                  f_1 \\  
                  ...\\
                  a_n
 \end{bmatrix} 
 \begin{bmatrix}  0 & 1 & 2 & ... n
 
 \end{bmatrix} 
 ```
 ```math
 signal_{matrix}= 
 \frac{f2\pi}{sample\_rate} 
 \begin{bmatrix}  0f_0 & 1f_0 & 2f_0 &... & nf_0\\  
                  0f_1 & 1f_1 & 2f_1 &... & nf_0\\  
                  ...\\
                  0f_n & 1f_n & 2f_n &... & nf_n\\  
 \end{bmatrix} 
```


```math 
signal_{matrix} = 
\begin{bmatrix}  \frac{0f_0f2\pi}{sample\_rate} & \frac{1f_0f2\pi}{sample\_rate} & \frac{2f_0f2\pi}{sample\_rate}& ... & & \frac{nf_0f2\pi}{sample\_rate}\\  
                  \frac{0f_1f2\pi}{sample\_rate} & \frac{1f_1f2\pi}{sample\_rate} & \frac{2f_1f2\pi}{sample\_rate}& ... & & \frac{nf_1f2\pi}{sample\_rate}\\  
                  ...\\
                  \frac{0f_nf2\pi}{sample\_rate} & \frac{1f_nf2\pi}{sample\_rate} & \frac{2f_nf2\pi}{sample\_rate}& ... & & \frac{nf_nf2\pi}{sample\_rate}\\  
 \end{bmatrix}
```

Verify this below:

```math 
signal = flatten(signal_{matrix})= 
\begin{bmatrix}   signal_{matrix}(1,1)&
                  signal_{matrix}(1,2)&
                  ...&
                  signal_{matrix}(2,1)&
                  signal_{matrix}(2,2)&
                  ...&
                  signal_{matrix}(n,m)
 \end{bmatrix}
```

```math
fourier\_series_{matrix} = sin(signal) \cdot ampl\_coefficients 

```
```math
fourier\_series_{matrix} = sin(
\begin{bmatrix}   \frac{nf_0f2\pi}{sample\_rate}
                  ...
                  \frac{nf_1f2\pi}{sample\_rate}
                  ...
                   \frac{nf_nf2\pi}{sample\_rate}  
 \end{bmatrix})
 \begin{bmatrix}  a_0 \\  
                  a_1 \\  
                  ...\\
                  a_n
 \end{bmatrix}
 
 
```
```math
fourier\_series_{matrix} = 
 \begin{bmatrix}  signal_{1,1} & signal_{1,2}
                  \frac{0f_1f2\pi}{sample\_rate} & \frac{1f_1f2\pi}{sample\_rate} & \frac{2f_1f2\pi}{sample\_rate}& ... & & \frac{nf_1f2\pi}{sample\_rate}\\  
                  ...\\
                  \frac{0f_nf2\pi}{sample\_rate} & \frac{1f_nf2\pi}{sample\_rate} & \frac{2f_nf2\pi}{sample\_rate}& ... & & \frac{nf_nf2\pi}{sample\_rate}\\  
 \end{bmatrix}
```


![Image of various signals](https://github.com/MartinTykhelle/SynthPy/blob/main/synth.py.png?raw=true)

