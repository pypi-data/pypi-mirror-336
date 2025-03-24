
# tutorials index

## t1.1: 這是第一個教學

## t1.2: 這是第二個教學


# 安裝指南

=== "FinLab 實驗室"
    ```
    打開選股策略頁面
    https://ai.finlab.tw/strategies
    並點選「建立策略」即可開始使用。
    ```

=== "Google Colab"
    ```python
    # 打開 Colab: https://colab.research.google.com/ 新增筆記本
    # 在 Colab 中任意 Cell 中執行

    !pip install finlab > log.txt

    # 即可
    ```

=== "本機 Python"
    ```python
    # 在 anacnoda prompt 中執行

    pip install finlab
    ```

    !!! tip "可能存在相容性問題"
        用「pip install finlab」方法安裝，可能會造成 Package 不相容的問題，
        假如您希望得到更穩定的版本，請參考「Docker」安裝。

=== "Docker 安裝"
    ### 1. 安裝 Docker
    
    請按照下列步驟安裝 Docker：

    * 前往 Docker 官方網站：https://www.docker.com/products/docker-desktop。
    * 在下載頁面中，按一下「Download Docker Desktop」按鈕。
    * 完成下載後，執行安裝程式並按照提示進行安裝。

    ### 2. 下載 FinLab 的 Jupyter 映像檔

    在安裝 Docker 完成後，請按照以下步驟從 Docker Hub 下載 FinLab 的 Jupyter 映像檔：

    開啟終端機或命令提示字元。

    輸入以下命令以下載 FinLab 的 Jupyter 映像檔：

    ```bash
    docker pull finlab/jupyter-finlab
    ```

    ### 3. 執行映像檔

    下載完成後，您可以使用以下命令執行映像檔：

    ```bash
    docker run -p 8888:8888 finlab/jupyter-finlab
    ```

    此命令將會啟動一個容器並將容器內部的 8888 埠口映射到您的本機 8888 埠口。
    請耐心等待容器啟動完成，終端機中將會顯示一個 URL，例如：

    ```
    http://127.0.0.1:8888/
    ```

    ### 4. 使用 JupyterLab

    在瀏覽器中打開剛剛複製的 URL，即可開始使用 FinLab。