# roborambo

Dead simple LLM-augmented Assistant/Bot system

```sh
git clone https://gacrc-sourcecontrol-01.gacrc.uga.edu/stanier/nothingburger.git
git clone https://gacrc-sourcecontrol-01.gacrc.uga.edu/stanier/roborambo.git

mkdir -p ~/.config/{nothingburger,roborambo}
cp -R ./nothingburger/examples/config/* ~/.config/nothingburger/
cp -R ./roborambo/examples/config/* ~/.config/roborambo

pip install --user ./nothingburger ./roborambo ./roborambo[zulip]

rambo-cli --assistant "Son of Rambo"
```
![alt text](assets/image.png)