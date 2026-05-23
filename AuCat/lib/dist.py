
import numpy as np

# Distance entre deux vecteurs complexes
def dist(vecA, vecB, saveur=0):
    if saveur == 0:
        return euleur_dist(vecA, vecB)
    if saveur == 1:
        return cosine_dist(vecA, vecB)


def euleur_dist(vecA, vecB):
    vector_A = np.array(vecA)
    vector_B = np.array(vecB)
    

    return np.linalg.norm(vector_A - vector_B)

def cosine_dist(vecA, vecB):
    """
    Calculates the cosine distance between two complex vectors.
    Returns a real number between 0 and 2.
    """
    vector_A = np.array(vecA)
    vector_B = np.array(vecB)

    # np.vdot(A, B) computes the complex inner product: sum(conj(A) * B)
    inner_product = np.vdot(vector_A, vector_B)

    norm_A = np.linalg.norm(vector_A)
    norm_B = np.linalg.norm(vector_B)

    # Cosine similarity for complex vectors
    cosine_similarity = inner_product / (norm_A * norm_B)

    # Distance is defined as 1 - real_part(similarity)
    # We take the real part because any tiny residual imaginary part is just numerical noise
    return 1.0 - np.real(cosine_similarity)
