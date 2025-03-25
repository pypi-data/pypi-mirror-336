# Twisted Torus Model of Grid Cells
This repo contains code to instantiate a twisted torus model of grid cell activity. This model is based on work by Guanella et al. 2007 [[1]](#1) but includes two additions: sources of noise and landmark input. Model details are included below.

## Getting started
### Running on Google Colab
You can try out the model without having to install anything by running this Google Colab <a target="_blank" href="https://colab.research.google.com/github/johnhwen1/ttgc/blob/main/examples/ttgc.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>. Alternatively, you can install the model locally and run the same example notebook (see below for instructions).

### Installing and running locally
1. Create a virtual environment (optional)
   1. If you have an Anaconda distribution of Python, create an environment with ```conda create --name ttgc python=3.11```. However, Python 3.9 or greater should work. Then, activate the environment with ```conda activate ttgc```
   2. If you use venv, first ensure you have Python 3.9 or greater installed. Then, navigate to a directory where you want to create the environment. If you have Python 3.11, you can run ```python3.11 -m venv ttgc```. Replace the version with the one you have. Then, activate your environment with either ```ttgc\Scripts\activate.bat``` if you're using Command Prompt on Windows or ```source ttgc/bin/activate``` if you're on macOS/Linux. 

2. Set up for GPU acceleration (optional). Some of the computations are intensive and benefit from GPU acceleration. If you have access to a GPU and want to use it, make sure you have the GPU version of pytorch installed. If the CPU version is installed, simply remove it with ```pip uninstall torch```. Then, run ```pip install torch --index-url https://download.pytorch.org/whl/cu126```. This will install pytorch with CUDA 12.6. You may need to run the following commands as well: ```pip install nvidia-pyindex``` and ```pip install nvidia-cuda-runtime-cu12```. If this fails, you might need to check your NVIDIA driver for the GPU and that the toolkit CUDA 12.6 is installed (to check, you can run ```nvcc --version```). Note that if you're running the Google Colab version above, you can use the GPU provided by Google. See notebook for details.

3. Install TTGC by pip installing or git clone / download.
   1. Method 1: Pip install directly from PyPI. Pip install by running ```pip install ttgc```. Then, you can download and run ttgc.ipynb in the [examples](https://github.com/johnhwen1/ttgc/examples) folder.
   2. Method 2: Git clone (or download). Git clone or download this repo, cd into the downloaded repo, and then run ```pip install .``` and ```pip install -r requirements.txt```.
Then, navigate to the examples folder and run the ttgc.ipynb 

## Model details
### Activity and Stabilization
A set of $N$ comodular grid cells's activity is modeled. The activity of neuron $i$ at time $t$ is given by the following:

<p align="center">
$A_i(t) = B_i(t) + \tau\bigg(\frac{B_i(t)} {{< B_j(t-1) >}_{j=1}^{N}} - B_i(t)\bigg),$
</p>

where $\tau$ represents a stabilization factor, ${< \space .\space>}_{j=1}^{N}$ is the mean over cells in the network, and $B_i(t)$ is a linear transfer function defined as follows:

<p align="center">
$B_i(t) = A_i(t-1) + \sum_{j=1}^{N}A_j(t-1)w_{ji}(t-1)$
</p>

where $w_{ji}(t-1)$ is the weight from cell $j$ to cell $i$ at time $t-1$, with $i,j \in \lbrace 1, 2, ..., N\rbrace$.

Neurons are initialized with random activity uniformly between $0$ and $1/\sqrt N$

### Attractor Dynamics
When the agent is stationary, the weight between neuron $i$ and $j$ is defined as follows:

<p align="center">
$w_{ij} = I \exp \bigg(- \frac{\|c_i - c_j\|^2_{tri}} {\sigma^2}\bigg) - T$
</p>

The weight is dependent on the relative "positions" of cells $i$ and $j$. The position of neuron $i$ is defined as ${c_i} = (c_{i_{x}}\space ,\space c_{i_{y}}),$ where $c_{i_{x}} = (i_x− 0.5)/N_x,$ and $c_{i_{y}} = \frac{\sqrt3}{2} (i_y− 0.5)/N_y$ with $i_x \in \lbrace1, 2, ..., N_x\rbrace$ and $i_y \in \lbrace1, 2, ..., N_y\rbrace$, and where $N_x$ and $N_y$ are the number of columns and rows in the cells matrix and $i_x$ and $i_y$ the column and the row numbers of cell $i$. 

Additionally, global parameters that govern the relationship between all pairs of cells include $I$, the intensity parameter, $\sigma$ the size of the Gaussian, $T$ the shift parameter (see the referenced paper for more details).

Finally, the key to getting triangular grid instead of square ones is to use a distance metric defined as follows: 
<p align="center">
$\text{dist}_{tri}(c_i, c_j)$ := $\| c_i - c_j\|_{tri} = \text{min}_{k=1}^7 \| c_i − \space  c_j +  \space s_k\|,$ 
</p>

where

$s_1 := (0, 0)$

$s_2 := (−0.5, \frac{\sqrt3}{2})$

$s_3 := (−0.5, -\frac{\sqrt3}{2})$

$s_4 := (0.5, \frac{\sqrt3}{2})$

$s_5 := (0.5, -\frac{\sqrt3}{2})$

$s_6 := (−1, 0)$

$s_7 := (1, 0)$

<p align="left">
and where $\|.\|$ is the Euclidean norm.
</p>

### Modulation
When the agent is moving, the weight between neurons $i$ and $j$ becomes modulated by the velocity $v := (v_x, v_y)$. In essence, the synaptic connections of the network shift in the direction of the agent. This modulation is expressed as follows:

<p align="center">
$w_{ij}(t) =  I \exp \bigg(- \frac{\|c_i - c_j+ \alpha R_{\beta}v(t-1)\|^2_{tri}} {\sigma^2}\bigg) - T$
</p>

The scale and orientation of the grid is dictated by the gain factor $\alpha \in \mathbb{R}^+$ and bias $\beta \in [0, \frac{\pi}{3}]$. The input of the network is thus modulated and biased by the gain and the bias parameters, with $v \longmapsto \alpha R_{\beta}v$ , where $R_{\beta}$ is the rotation matrix of angle $\beta$.

### Modifications
This model is modified in two key ways from the model described in Guanella et al 2007. The first modification allows for added heading direction noise at each timestep, and the second introduces landmark inputs to the grid cell network. Heading direction noise is added as $\beta_{\text{noisy}}(t) = \beta + \sigma_{\beta} r(t)$, where $\beta$ is the unmodified bias, $\sigma_{\beta}$ regulates the extent of noise, and $r(t)$ is drawn from the standard normal distribution, and $\beta_{\text{noisy}}(t)$ is still constrained such that $\beta_{\text{noisy}}(t) \in [0, \frac{\pi}{3}]$. The rotation matrix is then calculated using $\beta_{\text{noisy}}(t)$.

Landmark inputs are added with the addition of landmark cells and their unidirectional excitatory synaptic connections to grid cells. When landmarks are present, each landmark $L_{l}$ is associated with its own dedicated landmark cell population. A given landmark cell's activity $A_{L_{l_m}}$ is dependent on the agent's proximity to the landmark's position, where $l \in \lbrace1, ..., N_L\rbrace$ and where $N_L$ is the number of landmarks present and $m \in \lbrace1, ..., N_{Ln}\rbrace$ where $N_{Ln}$ is a global parameter setting the number of landmark cells dedicated to any given landmark. The activity of landmark cell $A_{L_{l_m}}$ is defined as follows:
<p align="center">
$A_{L_{l_m}} = \alpha_{L_l} \exp \bigg(- \frac{\|p(t) - p_{L_l}\|^2} {\big(\frac{1}{2} q_{L_l}\big)^2} \bigg) \text{if} \|p(t) - p_{L_l}\| \leq q_{L_l} \text{, and otherwise set to } 0$.
</p>

where the strength of landmark $L_l$ is governed by $\alpha_{L_l} \in \mathbb{R}^+$, $p(t):= (p_x(t), p_y(t))$ is the position of the agent at time $t$, $p_{L_l} := (p_{L_{l_x}}, p_{L_{l_y}})$ is the position of $L_l$, and $q_{L_l} \in \mathbb{R}^+$ represents the lookahead distance at which landmark $L_l$ begins recruiting the activity of its landmark cells. To incorporate input from landmark cells, the linear transfer function is modified as follows:

<p align="center">
$B_i(t) = A_i(t-1) + \sum_{j=1}^{N}A_j(t-1)w_{ji}(t-1) + \sum_{l=1}^{N_{L}} \sum_{m=1}^{N_{Ln}} A_{L_{l_m}}(t-1) w_{l_m i}(t-1)$
</p>

where $w_{l_mi}$ is the weight from landmark cell $m$, which responds to landmark $l$, to grid cell $i$.

## References
<a id="1">[1]</a>
Guanella, A., Kiper, D. & Verschure, P. 
A model of grid cells based on a twisted torus topology. 
Int. J. Neural Syst. 17, 231–240 (2007).
