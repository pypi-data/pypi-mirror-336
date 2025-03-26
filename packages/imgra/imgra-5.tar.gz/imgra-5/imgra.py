# # Image processing with graphs
#
# Most of this code is independent of images, and works for functions
# defined on arbitrary graphs.  Image processing is a particular case
# when the graph in question is a grid-graph.

# ## Graphs and matrices
#
# A directed, weighted graph is represented by its *signed incidence matrix*.
# This matrix has one column for each vertex, and one row for each edge.
# On each row, there are numbers -1 and +1 indicating the source and
# destination of the corresponding edge.
#
# This signed incidence matrix is also called the discrete gradient.
# The negative transpose of the discrete gradient is the discrete divergence.
# The divergence of the gradient is the laplacian, which is thus a symmetric,
# negative semidefinite matrix.
# The adjacency matrix is the laplacian without its diagonal.
# The structure matrix is the adjacency matrix plus the identity.
#
# Thus, all the matrices of the graph can be computed easily from the
# incidence matrix.  The converse is not true, because the ordering of the
# edges is arbitrary.  This justifies the choice of the incidence matrix as
# the main representation of a graph.
#
# Notice that there is only one true laplacian, always defined as Δ=-B'B,
# where B is the signed incidence matrix.  The various laplacian
# "normalizations" that you may find elsewhere correspond to different
# weightings of the incidence matrix.

def laplacian_from_incidence(B):
	L = - B.T @ B
	return L

def adjacency_from_incidence(B):
	A = - B.T @ B
	A.setdiag(0)
	return A

def structure_from_incidence(B):
	E = - B.T @ B
	E.setdiag(1)
	return E

# ## Mathematical morphology
#
# Mathematical morphology is a collection of local non-linear filters.  In
# modern parlance, a set of CNN neurons.  They have two slightly different
# implementations, depending on whether the images are binary or gray-level.
# In all cases, the operation consists in multiplying by the structure matrix
# and composing with a non-linear threshold.
#
# Mathematical morphology on binary images is done by multiplying the image
# by the structure matrix, and thresholding the result.  The erosion,
# dilation, and median filtering are obtained by using the min, max or middle
# values of the output as thresholds.

def binary_morphology_dilation(E, x):
	y = E @ x
	d = y > 0
	return d

def binary_morphology_erosion(E, x):
	y = E @ x
	e = 1 - (y < y.max())
	return e

def binary_morphology_median(E, x):
	y = E @ x
	m = y > y.max()/2
	return m

# Gray-level dilation is done by finding the maximum on each neighborhood
# defined by the graph.  This is equivalent to multiply by the structure
# matrix and pick the max of each row.  The other gray-level morphological
# operations are defined in terms of the dilation

def dilation_gray(E, x):
	from scipy.sparse import diags
	y = (diags(x.squeeze()) @ E).max(axis=0).A.T.squeeze()
	# TODO: make this formula work also for color data
	return y

def dilation_color(E, x):
	from numpy import vstack
	d =  x.squeeze().shape[1]
	y = vstack([dilation_gray(E, x[:,i]) for i in range(d)]).T
	return y

def dilation(E, x):
	if x.squeeze().ndim == 1 :
		return dilation_gray(E, x)
	else:
		return dilation_color(E, x)

# TODO: remove unnecessary sqeezes in the previous three functions


def erosion(E, x):
	m = 1 + x.max()
	t = m - x
	y = m - dilation(E, t)
	return y


# TODO: add docstrings for all these filters and explain what they are for
# TODO: add median filter (different implementation, parity choices)
def opening(E, x):      return dilation(E, erosion(E, x))
def closing(E, x):      return erosion(E, dilation(E, x))
def egradient(E, x):    return x - erosion(E, x)
def igradient(E, x):    return dilation(E, x) - x
def cgradient(E, x):    return (igradient(E,x) + egradient(E,x))/2
def mlaplacian(E, x):   return (igradient(E,x) - egradient(E,x))/2
def msharpen(E, x):     return x - mlaplacian(E, x)
def mblur(E, x):        return x + mlaplacian(E, x)
def tophat(E, x):       return x - opening(E, x)
def bothat(E, x):       return closing(E, x) - x
def oscillation(E, x):  return closing(E, x) - opening(E, x)
def iblur(E, x):        return (x + erosion(E, x))/2
def eblur(E, x):        return (x + dilation(E, x))/2
def cblur(E, x):        return (iblur(E, x) + eblur(E, x))/2


# ## Linear operators
#
# Linear operators are obtained by multiplication by the matrices of the
# graph.  Thus, there is no need to write special functions with them.
# We give them as a sort of documentation.  The underlying graph is always
# defined by its signed incidence matrix B.

def gradient(B, f):    return B @ f
def divergence(B, X):  return -B.T @ X
def laplacian(B, f):   return -B.T @ B @ f

# Some pointwise operators:

def pointwise_product_of_two_functions(B, f, g):
	return f * g

def scalar_product_of_function_and_field(B, f, X):
	C = abs(B)/2
	return (C @ f) * X
	return fX

def dot_product_of_two_fields(B, X, Y):
	C = abs(B)/2
	return C.T @ (X * Y)

def directional_derivative(B, X, f):
	return dot_product_of_two_fields(X, gradient(B, f))
	#C = abs(B)/2
	#return C.T @ (X * (B @ f))

# Integrals and flows are defined as dot products with indicator functions
# Notice that with these definitions, Green's formula (or Stokes) becomes
# just matrix associativity:
# $$\int_{\partial\Omega}X=\int_\Omega\mathrm{div} X\ \iff\ (-B\mathbf{1}_\Omega)^\top\cdot  X=\mathbf{1}_{\Omega}^\top\cdot(-B^\top X)$$


def integral(B, m, f):
	return m.T @ f

def flow(B, Γ, X):
	return Γ.T @ X

def boundary(B, m):
	Γ = -B @ m
	return Γ

# ## Poisson equation
#

def poisson_equation(
		B, # incidence matrix of the graph
		f, # target laplacian
		g, # boundary condition
		m  # mask
		):
	from scipy.sparse import diags, eye
	from scipy.sparse.linalg import spsolve

	L = -B.T @ B             # laplacian operator
	M = diags(m)             # mask operator
	I = eye(*L.shape)        # identity operator
	A = (I - M)     - M @ L  # linear system: matrix
	b = (I - M) @ g - M @ f  # linear system: constant terms
	u = spsolve(A, b)        # linear system: solution
	return u


# clone f into g inside m, using gradient merge criterion "s"
def poisson_editor(
		B, # incidence matrix of the graph
		f, # source image
		g, # destination image
		m, # mask
		s  # fusion criterion
		):
	if type(s) == str and s == "copypaste":
		return m*f + (1-m)*g

	L = -B.T @ B             # laplacian operator
	F = B @ f                # gradient of source image
	G = B @ g                # gradient of destination image

	# combine both gradients into a target gradient X
	if s == "replace":  X = F
	if s == "sum":      X = F + G
	if s == "average":  X = (F + G)/2
	if s == "max":      X = F + (G - F) * (abs(G) > abs(F))

	# recover the image from this gradient
	u = poisson_equation(B, -B.T @ X, g, m)
	return u


# call poisson editor separately for each color band
def poisson_editor_color(B, f, g, m, s):
	from numpy import dstack
	return dstack([
			poisson_editor(B, f[:,i], g[:,i], m, s)
			for i in range(f.shape[1])
		])


# ## Graph for images
#
# This function builds the B matrix of a grid graph, which is a natural
# domain for image processing.

def grid_incidence(h, w):
	""" Build the signed incidence matrix of a WxH grid graph """
	from scipy.sparse import eye, kron, vstack
	x = eye(w-1, w, 1) - eye(w-1, w)             # path graph of length W
	y = eye(h-1, h, 1) - eye(h-1, h)             # path graph of length H
	p = kron(eye(h), x)                          # H horizontal paths
	q = kron(y, eye(w))                          # W vertical paths
	B = vstack([p, q])                           # union of all paths
	return B

def pgrid_incidence(h, w):
	""" Build the signed incidence matrix of a WxH periodic grid graph """
	from scipy.sparse import eye, kron, vstack
	x = eye(w, w, 1) - eye(w, w)             # cycle graph of length W
	y = eye(h, h, 1) - eye(h, h)             # cycle graph of length H
	import warnings
	with warnings.catch_warnings(action="ignore"):
		x[-1,0] = 1
		y[-1,0] = 1
	p = kron(eye(h), x)                          # H horizontal paths
	q = kron(y, eye(w))                          # W vertical paths
	B = vstack([p, q])                           # union of all paths
	return B




# ## Examples
#
def demo_poisson_gray():
	# load source, destination and mask images for poisson editing
	import iio
	U = "http://gabarro.org/img/"
	f = iio.read(f"{U}poisson_source.png")[:,:,1]
	g = iio.read(f"{U}poisson_dest.png")[:,:,1]
	m = iio.read(f"{U}poisson_trimap.png")[:,:] > 0
	iio.gallery([f, g, m*127])

	h,w = f.shape
	f = f.flatten()
	g = g.flatten()
	m = m.flatten().astype(float)
	B = grid_incidence(h,w)

	T = list(range(5))
	T[0] = poisson_editor(B, f, g, m, "copypaste")
	T[1] = poisson_editor(B, f, g, m, "replace")
	T[2] = poisson_editor(B, f, g, m, "sum")
	T[3] = poisson_editor(B, f, g, m, "max")
	T[4] = poisson_editor(B, f, g, m, "average")
	T = [t.reshape(h,w) for t in T]
	iio.gallery(T)


def demo_poisson_color():
	# load source, destination and mask images for poisson editing
	import iio
	U = "http://gabarro.org/img/"
	f = iio.read(f"{U}poisson_source.png")
	g = iio.read(f"{U}poisson_dest.png")
	m = iio.read(f"{U}poisson_trimap.png") > 0
	iio.gallery([f, g, m*127])

	h,w,d = f.shape
	f = f.reshape(h*w, d)
	g = g.reshape(h*w, d)
	m = m.reshape(h*w).astype(float)
	B = grid_incidence(h,w)

	T = list(range(5))
	T[0] = poisson_editor_color(B, f, g, m, "copypaste")
	T[1] = poisson_editor_color(B, f, g, m, "replace")
	T[2] = poisson_editor_color(B, f, g, m, "sum")
	T[3] = poisson_editor_color(B, f, g, m, "max")
	T[4] = poisson_editor_color(B, f, g, m, "average")
	T = [t.reshape(h,w,d) for t in T]
	iio.gallery(T)


version = 5
# no need for __all__ since there's no hidden stuff


# vim:set tw=77 filetype=python spell spelllang=en:

def demo_morphology():
	import iio
	U = "http://gabarro.org/img/"
	x = iio.read(f"{U}barbara.png")[:,:,0]
	h,w = x.shape
	x = x.reshape(h*w)
	iio.gallery([x])

#demo_morphology()
#
#import iio
#x = iio.read("http://gabarro.org/img/barbara.png")
#
#h,w,d = x.shape
#x = x.reshape(h*w,d)
#
#iio.display(x)
#
#import iio
#
#iio.version








