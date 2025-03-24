import os
import re
import numpy as np
import matplotlib.pyplot as plt
import torch

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def visualize_attention_maps(model, dataloader, save_dir, device):
    print("Visualizing attention maps...")
    
    with torch.no_grad():
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        outputs = model.vit(pixel_values=dummy_input, output_attentions=True)
        num_layers = len(outputs.attentions)
        num_heads = outputs.attentions[0].shape[1]

    for batch_idx, batch in enumerate(dataloader):
        images, _ = batch
        images = images.to(device)
        with torch.no_grad():
            outputs = model.vit(pixel_values=images, output_attentions=True)
            attentions = outputs.attentions

            for layer_idx in range(num_layers):
                for head_idx in range(num_heads):
                    attention_weights = attentions[layer_idx][:, head_idx, :, :]
                    patch_attention = attention_weights[:, 1:, 1:]
                    patch_attention = patch_attention.cpu().numpy()
                    patch_size = 16
                    num_patches = int(np.sqrt(patch_attention.shape[1]))
                    patch_attention = patch_attention.reshape(-1, num_patches, num_patches)
                    patch_avg_attention = patch_attention.mean(axis=0)
                    patch_avg_attention = (patch_avg_attention - patch_avg_attention.min()) / (patch_avg_attention.max() - patch_avg_attention.min())
                    original_image = torch.mean(images, dim=0).cpu().numpy().transpose(1, 2, 0)

                    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=300)
                    axes[0].imshow(original_image)
                    axes[0].imshow(patch_avg_attention, cmap="viridis", alpha=0.6, extent=[0, 224, 224, 0])
                    axes[0].set_title(f"Patch-Averaged Attention\nLayer {layer_idx + 1}, Head {head_idx + 1}, Batch {batch_idx + 1}")
                    axes[0].axis("off")

                    overlay = np.zeros_like(original_image)
                    for i in range(num_patches):
                        for j in range(num_patches):
                            overlay[
                                i * patch_size : (i + 1) * patch_size,
                                j * patch_size : (j + 1) * patch_size,
                            ] = patch_attention[0, i, j]
                    axes[1].imshow(original_image)
                    axes[1].imshow(overlay, cmap="viridis", alpha=0.6)
                    axes[1].set_title(f"Overlay Attention Weights\nLayer {layer_idx + 1}, Head {head_idx + 1}, Batch {batch_idx + 1}")
                    axes[1].axis("off")

                    axes[2].imshow(original_image)
                    for i in range(num_patches):
                        for j in range(num_patches):
                            patch_num = i * num_patches + j
                            axes[2].text(
                                j * patch_size + patch_size // 2,
                                i * patch_size + patch_size // 2,
                                str(patch_num),
                                color="red",
                                fontsize=8,
                                ha="center",
                                va="center",
                            )
                    axes[2].set_title("Patch Locations on Original Image")
                    axes[2].axis("off")

                    figure_name = f"attention_visualization_layer_{layer_idx + 1}_head_{head_idx + 1}_batch_{batch_idx + 1}.png"
                    figure_name = sanitize_filename(figure_name)
                    figure_path = os.path.join(save_dir, figure_name)
                    try:
                        plt.tight_layout()
                        plt.savefig(figure_path, bbox_inches="tight", dpi=300)
                        plt.close()
                    except Exception as e:
                        print(f"Error saving figure {figure_path}: {e}")

    print(f"Attention visualizations saved to {save_dir}")