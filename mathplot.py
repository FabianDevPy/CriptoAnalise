
import matplotlib.pyplot as plt


def plot_crypto_data(data, title, save_path=None):
    # print(data)
    
    plt.figure(figsize=(10, 5))
    plt.plot(data['timestamp'], data['close'], marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel('Tempo')
    plt.ylabel('Preço (USD)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
        return save_path
    else:
        plt.show()