import numpy as np
import matplotlib.pyplot as plt

from test_3 import transform_to_camera, look_at, create_scene


def perspective_projection(vertices, focal_length):

    valid_mask = vertices[:, 2] > 0
    # if not np.any(valid_mask):
    #     raise ValueError("Nenhum vértice está na frente da câmera (z > 0).")

    valid_vertices = vertices[valid_mask]
    z = valid_vertices[:, 2]

    x_proj = (focal_length * valid_vertices[:, 0]) / z
    y_proj = (focal_length * valid_vertices[:, 1]) / z
    return np.column_stack((x_proj, y_proj)), valid_mask

def plot_2d_edges(vertices_2d, faces, valid_mask, color='b'):

    for face in faces:
        if np.all(valid_mask[face]):
            face_cycle = np.append(face, face[0])
            plt.plot(vertices_2d[face_cycle, 0],
                     vertices_2d[face_cycle, 1],
                     color=color, linewidth=1)

def plot_perspective_scene(scene, camera_rotation, camera_translation, focal_length=5):

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    plt.figure(figsize=(10, 8))
    plt.title("Projeção em Perspectiva 2D")
    plt.xlabel("X (2D)")
    plt.ylabel("Y (2D)")
    plt.grid(True)

    for idx, (verts, faces) in enumerate(scene):
        cam_verts = transform_to_camera(verts, camera_rotation, camera_translation)

        verts_2d, valid_mask = perspective_projection(cam_verts, focal_length)

        plot_2d_edges(verts_2d, faces, valid_mask, color=colors[idx % len(colors)])

    plt.show()

if __name__ == "__main__":
    scene = create_scene()

    camera_eye = np.array([15, 15, 15])
    camera_target = np.array([0, 0, 0])
    camera_up = np.array([0, 0, 1])

    camera_rotation, camera_translation = look_at(camera_eye, camera_target, camera_up)

    plot_perspective_scene(scene, camera_rotation, camera_translation, focal_length=5)