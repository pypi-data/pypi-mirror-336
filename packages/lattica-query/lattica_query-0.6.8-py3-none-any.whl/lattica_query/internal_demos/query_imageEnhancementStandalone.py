import torch
import matplotlib.pyplot as plt

from lattica_query.auth import get_demo_token
from lattica_query.lattica_query_client import QueryClient


model_id = "imageEnhancement"
# my_token = get_demo_token(model_id)
my_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZTRzBSMmVuWFYzZXJSR0pMaFFidSJ9.eyJ0b2tlbklkIjoiMmU5MzcxMTctMDgzZS00YTM4LWE2MTAtZGZmODE5MjFkZTAzIiwiaXNzIjoiaHR0cHM6Ly9kZXYtZjVrZ3Iwa25yd2pvYWF3MS51cy5hdXRoMC5jb20vIiwic3ViIjoiUFFJUVVpN24zbUpqSnBNdmFKRkQzQ09kTzRwMzVCc3ZAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vbXlhcGkvYXBpIiwiaWF0IjoxNzQyMzk0NjkyLCJleHAiOjE3NDQ5ODY2OTIsInNjb3BlIjoidXNlciBkZWZhdWx0IiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoiUFFJUVVpN24zbUpqSnBNdmFKRkQzQ09kTzRwMzVCc3YiLCJwZXJtaXNzaW9ucyI6WyJ1c2VyIiwiZGVmYXVsdCJdfQ.gelb9wcN2853e1RRMtXQ390XZ2wAe7gH8q9C3VsZLp5rHfNa664PvtMVxUg_tjLtwU_67sMY5pmwBUbJmmQpLVc938H0vu8zKVXRXwIkOd-Nh2Kq0QNokE0csy3Rf5cNWvcdcXxzDRgYB7AYXA4FZi0jEL-8N637eCwvxFzfgn8oGFe3327flG8f-imJvCyxANv9VTtjkC0JZd9dLetZ8EfNExi-a1znM8i59CKGRRg-2gzFOBOcq2Vw_VfN8MfPhoizfXcmCQn_u2qZencWTO3W86XbLjMd90bmKurUytocnU8VY4R0Fs4f-WssYRbhtrw3wJRts2t1SXViDlWZoQ"

client = QueryClient(my_token)

# OFFLINE PHASE
(
    serialized_context,
    serialized_secret_key,
    serialized_homseq,
) = client.generate_key()

# ONLINE PHASE
xxx = plt.imread('house_200x200.png')[..., :3]
pt = torch.tensor(xxx, dtype=torch.float64).moveaxis(-1, 0)  # (C, H, W)

pt_dec = client.run_query(serialized_context, serialized_secret_key, pt, serialized_homseq)

# For debugging: apply pipeline in the clear
pt_expected = client.apply_clear(pt)

# Verify similarity
fig, ax = plt.subplots(1, 2)
ax[0].imshow(pt.permute(1, 2, 0), cmap="gray")
ax[0].set_title("original image")
ax[0].axis("off")
ax[1].imshow(pt_dec.permute(1, 2, 0), cmap="gray")
ax[1].set_title("homomorphic sharpen")
ax[1].axis("off")
plt.show()

print(f"{pt_expected.shape=} {pt_dec.shape=}")