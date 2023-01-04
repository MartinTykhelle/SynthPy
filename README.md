# SynthPy
Synth for Pi Pico written in Circuitpython

## Math

### Declarations
The fourier series coefficients are declared as $f_{0-n}$ and $a_{0-n}.

$$
 freq\_coefficients = \begin{bmatrix}  f_0 \\  
                  f_1 \\  
                  ...\\
                  f_n
 \end{bmatrix}
 $$
 
$$
 ampl\_coefficients = \begin{bmatrix}  a_0 \\  
                  a_1 \\  
                  ...\\
                  a_n
 \end{bmatrix}
$$
The length of the series, $k$ is defined as  $floor(\frac{sample\_rate}{frequency})$
$$
 i = 
 \begin{bmatrix}  0 & 1 & 2 & ... k
 \end{bmatrix}
$$


### Signal Matrix
$$
 signal = \frac{f2\pi}{sample\_rate} \cdot freq\_coefficients \cdot i  
$$
$$
signal= 
 \frac{f2\pi}{sample\_rate} 
 \begin{bmatrix}  f_0 \\  
                  f_1 \\  
                  ...\\
                  a_n
 \end{bmatrix} 
 \begin{bmatrix}  0 & 1 & 2 & ... k
 
 \end{bmatrix} 
$$
$$
 signal= 
 \frac{f2\pi}{sample\_rate} 
 \begin{bmatrix}  0f_0 & 1f_0 & 2f_0 &... & kf_0\\  
                  0f_1 & 1f_1 & 2f_1 &... & kf_0\\  
                  ...  & ...  & ...  &... & ... \\
                  0f_n & 1f_n & 2f_n &... & kf_n\\  
 \end{bmatrix} 
$$

Eventually this will turn out like this, each row of the matrix contains one fourier series.
$$
signal = 
\begin{bmatrix}  \frac{0f_0f2\pi}{sample\_rate} & \frac{1f_0f2\pi}{sample\_rate} & \frac{2f_0f2\pi}{sample\_rate}& ... &  \frac{kf_0f2\pi}{sample\_rate}\\  
                  \frac{0f_1f2\pi}{sample\_rate} & \frac{1f_1f2\pi}{sample\_rate} & \frac{2f_1f2\pi}{sample\_rate}& ... &  \frac{kf_1f2\pi}{sample\_rate}\\  
                  ...  & ...  & ...  &... & ... \\
                  \frac{0f_nf2\pi}{sample\_rate} & \frac{1f_nf2\pi}{sample\_rate} & \frac{2f_nf2\pi}{sample\_rate}& ... &  \frac{kf_nf2\pi}{sample\_rate}\\  
 \end{bmatrix}
$$

### Fourier Series

$$
fourier\_series\_matrix = sin(signal) \cdot ampl\_coefficients 
$$
$$
fourier\_series\_matrix = sin(
 \frac{f2\pi}{sample\_rate} 
 \begin{bmatrix}  0f_0 & 1f_0 & 2f_0 &... & nf_0\\  
                  0f_1 & 1f_1 & 2f_1 &... & nf_0\\  
                  ...  & ...  & ...  &... & ... \\
                  0f_n & 1f_n & 2f_n &... & nf_n\\  
 \end{bmatrix} 
)
 \begin{bmatrix}  a_0 \\  
                  a_1 \\  
                  ...\\
                  a_n
 \end{bmatrix}
 
 
$$
$$
fourier\_series\_matrix = sin(
 \frac{f2\pi}{sample\_rate} 
 \begin{bmatrix}  0f_0a_0 & 1f_0a_1 & 2f_0a_3 &... & nf_0a_n\\  
                  0f_1a_0 & 1f_1a_1 & 2f_1a_3 &... & nf_1a_n\\  
                  ...     & ...     & ...     &... & ...    \\
                  0f_na_0 & 1f_na_1 & 2f_na_3 &... & nf_na_n\\  
 \end{bmatrix}
)
$$

The rows of the matrix are eventually summed to get the fourier_series
$$
fourier\_series =  \sum_{f=1}^{k} fourier\_series\_matrix
$$

$$
fourier\_series =  
 [
 sin(\frac{f2\pi0f_0a_0}{sample\_rate})+sin(\frac{f2\pi0f_1a_0}{sample\_rate})+...+sin(\frac{f2\pi0f_na_0}{sample\_rate})
 ,\\
 sin(\frac{f2\pi1f_0a_1}{sample\_rate})+sin(\frac{f2\pi1f_1a_1}{sample\_rate})+...+sin(\frac{f2\pi1f_na_1}{sample\_rate})
 ,\\
 ,...
 \\
 sin(\frac{f2\pi nf_0a_n}{sample\_rate})+sin(\frac{f2\pi nf_1a_n}{sample\_rate})+...+sin(\frac{f2\pi nf_na_n}{sample\_rate})
 ]
$$


![Image of various signals](synth.py.png?raw=true)

