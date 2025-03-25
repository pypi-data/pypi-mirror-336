import numpy as np
from compas.plugins import plugin

from test_my_binding.test_my_binding_ext import VectorRowMatrixXd
from test_my_binding.test_my_binding_ext import intersections

from .types import PolylinesNumpy
from .types import VerticesFaces


@plugin(category="intersections")
def intersection_mesh_mesh(
    A: VerticesFaces,
    B: VerticesFaces,
) -> PolylinesNumpy:
    """Compute the intersection of tow meshes.

    Parameters
    ----------
    A : :attr:`test_my_binding.types.VerticesFaces`
        Mesh A.
    B : :attr:`test_my_binding.types.VerticesFaces`
        Mesh B.

    Returns
    -------
    :attr:`test_my_binding.types.PolylinesNumpy`
        A list of intersection polylines, with each polyline an array of points.

    Examples
    --------
    >>> from compas.geometry import Box, Sphere, Polyline
    >>> from test_my_binding.intersections import intersection_mesh_mesh

    >>> box = Box(1)
    >>> sphere = Sphere(0.5, point=[1, 1, 1])

    >>> A = box.to_vertices_and_faces(triangulated=True)
    >>> B = sphere.to_vertices_and_faces(u=32, v=32, triangulated=True)

    >>> result = intersection_mesh_mesh(A, B)
    >>> polylines = [Polyline(points) for points in result]

    """
    VA, FA = A
    VB, FB = B
    VA = np.asarray(VA, dtype=np.float64, order="C")
    FA = np.asarray(FA, dtype=np.int32, order="C")
    VB = np.asarray(VB, dtype=np.float64, order="C")
    FB = np.asarray(FB, dtype=np.int32, order="C")

    pointsets: VectorRowMatrixXd = intersections.intersection_mesh_mesh(VA, FA, VB, FB)

    return pointsets
