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
 freq_coefficients = \begin{bmatrix}  a_0 \\  
                  a_1 \\  
                  ...\\
                  a_n
 \end{bmatrix}
```

```math
 signal = freq_coefficients \cdot i  = \begin{bmatrix}  f_0 \\  
                  f_1 \\  
                  ...\\
                  a_n
 \end{bmatrix} 
 \cdot
 \begin{bmatrix}  0 & 1 & 2 & ... n
 \end{bmatrix}
 = \begin{bmatrix}  f_0*0 & f_0*1 & f_0*2 &... & f_0*n\\  
                  f_1*0 & f_1*1 & f_1*2 &... & f_0*n\\  
                  ...\\
                  f_n*0 & f_n*1 & f_n*2 &... & f_n*n\\  
 \end{bmatrix}
```

Flattening signal and multiplying by 
```math 
\frac{f2\pi}{sample\_rate}
```
```math
\begin{bmatrix}  \frac{0f_0f2\pi}{sample\_rate} & \frac{1f_0f2\pi}{sample\_rate} & \frac{0f_0f2\pi}{sample\_rate} &... & f_0*n\\  
                  f_1*0 & f_1*1 & f_1*2 &... & f_0*n\\  
                  ...\\
                  f_n*0 & f_n*1 & f_n*2 &... & f_n*n\\  
 \end{bmatrix}
```
