# tool_script

## 环境配置
```bash
# 安装Python虚拟环境-search
conda create --name search python=3.10
conda activate search
pip install -r requirements_search.txt
# 安装Python虚拟环境-recommend
conda create --name recommend python=3.10
conda activate recommend
pip install -r requirements_recommend.txt
# 安装Python虚拟环境-qabot
conda create --name qabot python=3.10
conda activate qabot
pip install -r requirements_qabot.txt
# 链接云盘数据(使用自己的云盘路径)
ln -s /mnt/pfs-guan-ssai/nlu/xuzhou1/data data/cloud
# 链接数据卷-密云
ln -s /lpai/volumes/ss-sai-lx-my/xuzhou1/data data/cloud
ln -s /lpai/volumes/ss-sai-lx-my/xuzhou1/data_share data/cloud_share
# 链接数据卷-固安
ln -s /lpai/volumes/ss-sai-bd-ga/xuzhou1/data data/cloud
ln -s /lpai/volumes/ss-sai-bd-ga/xuzhou1/data_share data/cloud_share
```
