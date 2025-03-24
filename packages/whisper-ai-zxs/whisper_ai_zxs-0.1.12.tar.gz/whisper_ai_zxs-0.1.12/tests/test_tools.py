
from whisper_ai_zxs.whisper_tools import WhisperTools_UploadSellingProduct_Red

tools1 = WhisperTools_UploadSellingProduct_Red("Manreya小红书店")
tools1.analyze("/Users/lizhenhua/WeChatProjects/WhisperAI/tests/data/小红书商品库下载_Manreya小红书店.zip")
tools2 = WhisperTools_UploadSellingProduct_Red("植想说小红书店")
tools2.analyze("/Users/lizhenhua/WeChatProjects/WhisperAI/tests/data/小红书商品库下载_植想说小红书店.zip")