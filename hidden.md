## 说明 ##
* E5自动续期程序
* 996时间表，每小时启动一次
* 每天24时更新一次refresh_token
   
#### 微软方面的准备工作 ####

* **第一步，注册应用，获取应用id、secret**

    * 1）点击打开[仪表板](https://aad.portal.azure.com/)，左边点击**所有服务**，找到**应用注册**，点击+**新注册**
    
     ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/creatapp.png)
    
    * 2）填入名字，受支持账户类型前三任选，重定向填入 http://localhost:53682/ ，点击**注册**
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/creatapp2.png)
    
    * 3）复制应用程序（客户端）ID到记事本备用(**获得了应用程序ID**！)，点击左边管理的**证书和密码**，点击+**新客户端密码**，点击添加，复制新客户端密码的**值**保存（**获得了应用程序密码**！）
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/creatapp3.png)
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/creatapp4.png)
    
    * 4）点击左边管理的**API权限**，点击+**添加权限**，点击常用Microsoft API里的**Microsoft Graph**(就是那个蓝色水晶)，
    点击**委托的权限**，然后在下面的条例选中下列需要的权限，最后点击底部**添加权限**
    
    **赋予api权限的时候，选择以下几个**
  
                Calendars.ReadWrite、Contacts.ReadWrite、Directory.ReadWrite.All、
                
                Files.ReadWrite.All、MailboxSettings.ReadWrite、Mail.ReadWrite、
                
                Notes.ReadWrite.All、People.Read.All、Sites.ReadWrite.All、
                
                Tasks.ReadWrite、User.ReadWrite.All、SecurityEvents.Read.All
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/creatapp5.png)
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/creatapp6.png)
     
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/creatapp8.png)
    
    * 5）添加完自动跳回到权限首页，点击**代表授予管理员同意**
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/creatapp7.png)
    
* **第二步，获取refresh_token(微软密钥)**

    * 1）rclone.exe所在文件夹，shift+右键，在此处打开powershell，输入下面**修改后**的内容，回车后跳出浏览器，登入e5账号，点击接受，回到powershell窗口，看到一串东西。
           
                ./rclone authorize "onedrive" "应用程序(客户端)ID" "应用程序密码"
               
    * 2）在那一串东西里找到 "refresh_token"：" ，从双引号开始选中到 ","expiry":2021 为止（就是refresh_token后面双引号里那一串，不要双引号），如下图，右键复制保存（**获得了微软密钥**）
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApi/token地方.png)
    
 ____________________________________________________
 
 #### GITHUB方面的准备工作 ####

 * **第一步，fork本项目**
 
     登陆/新建github账号，回到本项目页面，点击右上角fork本项目的代码到你自己的账号，然后你账号下会出现一个一模一样的项目，接下来的操作均在你的这个项目下进行。
     
     ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApi/fork.png)
     
 * **第二步，新建github密钥**
 
    * 1）进入你的个人设置页面 (右上角头像 Settings，不是仓库里的 Settings)，选择 Developer settings -> Personal access tokens -> Generate new token

    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApi/Settings.png)
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApi/token.png)
    
    * 2）设置名字为 **GH_TOKEN** , 然后勾选repo，点击 Generate token ，最后**复制保存**生成的github密钥（**获得了github密钥**，一旦离开页面下次就看不到了！）
   
   ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/repo.png)
  
 * **第三步，新建secret**
 
    * 1）依次点击页面上栏右边的 Setting -> 左栏 Secrets -> 右上 New repository secret，新建4个secret： **GH_TOKEN、MS_TOKEN、CLIENT_ID、CLIENT_SECRET**  
   
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/setting.png)
    
    ![image](https://github.com/wangziyingwen/ImageHosting/blob/master/AutoApiP/secret2.png)
    
     **(以下填入内容注意前后不要有空格空行)**
 
     GH_TOKEN
     ```shell
     github密钥 (第三步获得)，例如获得的密钥是abc...xyz，则在secret页面直接粘贴进去，不用做任何修改，只需保证前后没有空格空行
     ```
     MS_TOKEN
     ```shell
     微软密钥（第二步获得的refresh_token）
     ```
     CLIENT_ID
     ```shell
     应用程序ID (第一步获得)
     ```
     CLIENT_SECRET
     ```shell
     应用程序密码 (第一步获得)
     ```
________________________________________________

#### 调用API ####
   
   点击项目上方的Actions，点击Auto Api Pro，点击Run workflow, 再点击绿色的Run workflow按钮
   
   ![image](https://user-images.githubusercontent.com/11155705/104392445-09493e00-557d-11eb-98f4-0e8308b7a1ba.png)
   
### 致谢 ###
[wangziyingwen/AutoApiP](https://github.com/wangziyingwen/AutoApiP)
