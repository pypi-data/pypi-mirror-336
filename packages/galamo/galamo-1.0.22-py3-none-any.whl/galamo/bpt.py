import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def draw(input_file, save_figure=False, output_filename="BPT_diagram.pdf"):
    """
    Draws the BPT diagram based on the input CSV file containing galaxy spectral data.
    
    Parameters:
    - input_file (str): Path to the CSV file.
    - save_figure (bool, optional): Whether to save the figure. Default is False.
    - output_filename (str, optional): Filename to save the figure. Default is "BPT_diagram.pdf".
    """
    required_columns = ['h_alpha_flux', 'h_beta_flux', 'oiii_5007_flux', 'nii_6584_flux',
                        'oi_6300_flux', 'sii_6717_flux', 'sii_6731_flux']
    
    # Read the data
    df = pd.read_csv(input_file)
    
    # Check if required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Define classification lines
    x = np.linspace(-2, 0, 20)
    y = (0.61/(x-0.05)) + 1.3
    x1 = np.linspace(-2, 0.4, 20)
    y1 = (0.61/(x1-0.47))+1.19
    x2 = np.linspace(-2, 0.1, 20)
    y2 = (0.72/(x2 -0.32))+1.3
    sx1 = np.linspace(-0.3, 1, 20)
    sy1 = 1.89 * sx1 + 0.76
    x3 = np.linspace(-2.5, -0.75, 20)
    y3 = (0.73/(x3+0.59))+1.33
    sx2 = np.linspace(-1.1, 0, 20)
    sy2 = 1.18 * sx2 + 1.30
    
    # Apply selection criteria
    mask_1 = 0.73/(np.log10(df['oi_6300_flux']/df['h_alpha_flux']) + 0.59) + 1.33 < np.log10(df['oiii_5007_flux']/df['h_beta_flux'])
    agn2_1 = df[mask_1]
    mask_2 = 0.61/(np.log10(agn2_1['nii_6584_flux']/agn2_1['h_alpha_flux']) - 0.47) + 1.19 < np.log10(agn2_1['oiii_5007_flux']/agn2_1['h_beta_flux'])
    agn2_2 = agn2_1[mask_2]
    mask_3 = 0.72/(np.log10((agn2_2['sii_6717_flux'] + agn2_2['sii_6731_flux'])/agn2_2['h_alpha_flux']) - 0.32) + 1.33 < np.log10(agn2_2['oiii_5007_flux']/agn2_2['h_beta_flux'])
    agn2 = agn2_2[mask_3]
    
    # Classify as Seyfert or LINER
    mask_liner = np.logical_or(
        1.18 * np.log10(agn2['oi_6300_flux']/agn2['h_alpha_flux']) + 1.3 > np.log10(agn2['oiii_5007_flux']/agn2['h_beta_flux']),
        1.89 * np.log10((agn2['sii_6717_flux'] + agn2['sii_6731_flux'])/agn2['h_alpha_flux']) + 0.76 > np.log10(agn2['oiii_5007_flux']/agn2['h_beta_flux'])
    )
    liner = agn2[mask_liner]
    seyf = agn2[~mask_liner]
    
    # Plot BPT diagrams
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    ax_titles = ['[NII] BPT', '[SII] BPT', '[OI] BPT']
    x_data = [
        np.log10(df['nii_6584_flux']/df['h_alpha_flux']),
        np.log10((df['sii_6717_flux'] + df['sii_6731_flux'])/df['h_alpha_flux']),
        np.log10(df['oi_6300_flux']/df['h_alpha_flux'])
    ]
    y_data = np.log10(df['oiii_5007_flux']/df['h_beta_flux'])
    class_x_data = [
        np.log10(seyf['nii_6584_flux']/seyf['h_alpha_flux']),
        np.log10((seyf['sii_6717_flux']+seyf['sii_6731_flux'])/seyf['h_alpha_flux']),
        np.log10(seyf['oi_6300_flux']/seyf['h_alpha_flux'])
    ]
    
    for i, ax in enumerate(axes):
        ax.scatter(x_data[i], y_data, alpha=0.1, marker='x', color='k')
        ax.scatter(class_x_data[i], np.log10(seyf['oiii_5007_flux']/seyf['h_beta_flux']), alpha=0.5, marker='o', color='r')
        ax.set_title(ax_titles[i])
        ax.set_xlabel(['log([NII]/Hα)', 'log([SII]/Hα)', 'log([OI]/Hα)'][i])
        ax.set_ylabel('log([OIII]/Hβ)')
    
    plt.tight_layout()
    
    # Save figure if needed
    if save_figure:
        plt.savefig(output_filename, bbox_inches='tight', pad_inches=0.1, transparent=True)
    
    plt.show()
