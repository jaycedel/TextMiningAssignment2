from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import nltk
import ssl

#https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download()

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    #print(chunked)
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    if continuous_chunk:
        named_entity = " ".join(current_chunk)
        if named_entity not in continuous_chunk:
            continuous_chunk.append(named_entity)

    return continuous_chunk

txt = "Audio Tool:   The GodFather  Audio Tool:   SoundEngine Free  Audio Tool:   MP3Gain  Internet Explorer Front-End:   SlimBrowser  Web browser:   Mozilla  PDF Utility:   Free PDF  Network Tool:   WinSCP  Partition Manager:   Ranish Partition Manager  File Manager:   JExplorer  Encryption and data security:   PGP Freeware  Pop-up Blocker:   NoAds  Network Tool:   RAS Graph & Stats  Pop-up Blocker:   Proxomitron  Anti-Virus:   AntiVir  Instant Messenger:   Miranda IM  Download manager:   wget  Firewall:   Sygate (FREE for personal use)  Audio Tool:   Rarewares  Pop-up Blocker:   Privoxy  Audio Tool:   MP3 Book Helper  CD/DVD Burning:   CDRDAO  Anti Spyware:   SpywareBlaster  Internet Explorer Front-End:   MyIE2  Anti-spam program:   SpamBayes  Download manager:   Fresh Download  Pop-up Blocker:   PopUp Stopper  Audio Tool:   MP3 Tag  File Manager:   A43  Audio Tool:   Audacity  Video player:   Media Player Classic  General Utilities And Other Application:   Celestia  Instant Messenger:   Gaim  Office Suite:   Open Office  General Utilities And Other Application:   Nullsoft Installer  General Utilities And Other Application:   Peerguardian  HTML Editor:   Selida  Video tool:   xviD  Audio Player:   QCD Player  Photo manipulation and image design:   Tuxpaint  PDF Utility:   PDF 995  Firewall:   Kerio (Kerio Personal Firewall is FREE for home and personal use)  Compression / Decompression:   bzip2  3D Graphic:   Anim8or  Encryption and data security:   Eraser  Network Tool:   TightVNC  Programming:   Freepascal  Audio Tool:   TagScanner  3D Graphic:   Now3D  PDF Utility:   Ghostscript/GSView  Encryption and data security:   GnuPG  System Information and monitoring:   AIDA32  Web browser:   Firebird  General Utilities And Other Application:   Inno Setup  Download manager:   Star Downloader  Audio Tool:   dBpowerAMP Music Converter  Anti-spam program:   K9  Partition Manager:   TestDisk  Audio Player:   Sonique  Anti-spam program:   POPFile  General Utilities And Other Application:   Sysinternals  Checksum Utilitie:   fsum  File Manager:   2xExplorer  Audio Player:   Winamp  Anti Spyware:   Diet K  Programming:   jEdit  Encryption and data security:   Axcrypt  Download manager:   wackget  Audio Player:   Musik  Web browser:   K-Meleon  General Utilities And Other Application:   AppRocket  Audio Tool:   CDex  File Manager:   MeeSoft Commander  Checksum Utilitie:   hksfv  Compression / Decompression:   7-zip  Audio Player:   Jet Audio Basic  Pop-up Blocker:   Google Toolbar  IRC Client:   BersIRC  Compression / Decompression:   UPX  HTML Editor:   HTML-Kit  CD/DVD Burning:   CDBurnerXP  Photo manipulation and image design:   Sodiodi  CD/DVD Burning:   Burn4Free  General Utilities And Other Application:   png2ico  3D Graphic:   gmax  FTP Client:   Filezilla!  IRC Client:   HydraIRC  Internet Explorer Front-End:   Avantbrowser  Web server:   Sambar  Checksum Utilitie:   md5summer  Anti-Virus:   AVG  Programming:   Python  Checksum Utilitie:   md5sum  Anti Spyware:   Ad-aware  Web server:   TinyWeb  Web server:   Apache  Audio Player:   1by1  Programming:   ActivePerl  Video tool:   GSpot  Instant Messenger:   PSI  HTML Editor:   Trellian webPAGE  Download manager:   LeechGet  System Information and monitoring:   Gkrellm  Webcam Software:   booruWebCam  3D Graphic:   Blender  Partition Manager:   Partition Resizer  Network Tool:   Ethereal Protocol Analyzer  Network Tool:   Ntop  Network Tool:   RealVNC  Compression / Decompression:   FilZip  CD/DVD Burning:   CDR Tools Frontend  HTML Editor:   AceHTML  File repair and recovery:   PC Inspector File Recovery  Image viewer:   SlowView  General Utilities And Other Application:   Cygwin  Video code:   Quicktime Alternative  Audio Tool:   KraMixer  Compression / Decompression:   UltimateZIP  Web browser:   Netscape  Image viewer:   Ahaview  Video tool:   VirtualDubMod  Audio Tool:   mp3Trim  Video tool:   VirtualDub  Encryption and data security:   Blowfish Advanced CS  HTML Editor:   TSW WebCoder  Desktop Enhancement:   tclock2  Compression / Decompression:   IZArc  Audio Player:   Foobar 2000  General Utilities And Other Application:   EditPad Lite  Compression / Decompression:   TUGZip  HTML Editor:   Aracnophilia  Audio Player:   iTunes  Video code:   DivX Codec  Download manager:   Net Transport  Video tool:   Zwei-Stein Video Editor  Firewall:   Zonealarm Basic firewall  File Manager:   Gyulas Navigator  Video code:   FFDSHOW  Mail program:   i.Scribe  System Information and monitoring:   CPU-Z  Compression / Decompression:   QuickZip  General Utilities And Other Application:   Dirkey  FTP Client:   SmartFTP  Instant Messenger:   Rhymbox  Video tool:   DVD Shrink  PDF Utility:   PDFCreator  Anti-spam program:   MailWasher  General Utilities And Other Application:   NetTime  General Utilities And Other Application:   Vim  FTP Server:   Quick n Easy FTP Server  Audio Tool:   Encounter 2003  Programming:   PHP Hypertext Parser  IRC Client:   BitchX  System Information and monitoring:   Motherboard monitor  Video player:   VideoLan  Programming:   Dev C++  Mail program:   Mahogany Mail  Desktop Enhancement:   MobyDock  Firewall:   Outpost Firewall (version 1 is free)  Encryption and data security:   WindowsCleaner  Audio Tool:   EAC  Video code:   Kazaa Lite Codec Pack  FTP Server:   WarFTPD  IRC Client:   TinyIRC  Video player:   Cygwin MPlayer  General Utilities And Other Application:   Memtest-86  Web server:   Abyss  CD/DVD Burning:   Burnatonce  Office Suite:   602PC Suite free edition  Video code:   Real Player Alternative  IRC Client:   XChat  Defrag Software:   OpenVMS  Audio Tool:   K-MP3  Programming:   SharpDevelop  Office Suite:   AbiWord  Network Tool:   UltraVNC  Video tool:   FlasKMPEG  Network Tool:   PuTTY  HTML Editor:   1st page 2000  Video player:   MaximusDVD  3D Graphic:   SOFTIMAGE|XSI EXP  Photo manipulation and image design:   ColorPic  CD/DVD Burning:   Easy Burning, DropCD & Audio CD  FTP Server:   GuildFTPD  Encryption and data security:   File Shredder  Anti Spyware:   SpywareGuard  FTP Server:   SlimFTPd  Webcam Software:   Pryme  3D Graphic:   Maya Personal Learning Ed.  CD/DVD Burning:   Deepburner  Audio Tool:   mp3DirectCut  General Utilities And Other Application:   Stickies  Network Tool:   CMDTime NTP Utility  General Utilities And Other Application:   AnalogX  Anti-Virus:   Avast  Programming:   Ruby  CD/DVD Burning:   DVD Decrypter:  Instant Messenger:   Trillian Basic  Image viewer:   Irfanview  Video code:   Nimo Codec Pack  Anti Spyware:   SpyBot Search & Destroy  Audio Tool:   MusicBrainz  Mail program:   Pegasus Mail  Image viewer:   XNView  Network Tool:   NMap  Photo manipulation and image design:   The Gimp  Network Tool:   PingPlotter  Photo manipulation and image design:   Pixia  Video player:   BsPlayer  Desktop Enhancement:   CursorXP  Mail program:   Thunderbird  FTP Server:   FileZilla  Compression / Decompression:   Zip&Go  General Utilities And Other Application:   MWSnap  Defrag Software:   DIRMS & Buzzsaw  General Utilities And Other Application:   QuickSFV  Video tool:   DScaler  Programming:   Eclipse  System Information and monitoring:   WCPUID  Programming:   Dev Pascal  Web server:   Savant  Compression / Decompression:   Zipgenius  Audio Tool:   GermaniXEncoder"
# print (get_continuous_chunks(txt))

for sent in nltk.sent_tokenize(txt):
    topics = {}
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
        if hasattr(chunk, 'label'):
            #print(chunk.label())
            if chunk.label() in topics:
                keyValue = topics[chunk.label()]
                if keyValue is not None:
                    keyValue.append(' '.join(c[0] for c in chunk))
                    topics[chunk.label()] = keyValue
                    print(topics[chunk.label()])
            else:
                # CREATE A NEW DICTIONARY WITH A VALUE LIST
                topics[chunk.label()] = [' '.join(c[0] for c in chunk)]
                #print(topics[chunk.label()])

    # for keyTopic in topics:
    #     print(keyTopic, '->', topics[keyTopic])