/**
 * NextFrame Authorization Bypass V2 - 完全绕过登录
 * 
 * 功能:
 * 1. Hook NSJSONSerialization 修改所有 API 响应
 * 2. Hook UserDefaults 伪造登录状态
 * 3. Hook AccountManager 相关方法
 * 4. 阻止显示登录界面
 * 5. 伪造所有权限检查
 * 
 * 编译: ./build.sh
 */

#import <Foundation/Foundation.h>
#import <AppKit/AppKit.h>
#import <objc/runtime.h>
#import <objc/message.h>

// ============================================================
// 配置
// ============================================================

static const NSInteger kRemainingExports = 999999;
static const NSInteger kMaxExports = 999999;
static const BOOL kSubscriptionActive = YES;
static const NSInteger kAccountValidDays = 36500;
static const NSInteger kMaxDevices = 999;

// ============================================================
// 日志
// ============================================================

#define LOG(fmt, ...) NSLog(@"[Bypass] " fmt, ##__VA_ARGS__)
#define LOG_HOOK(fmt, ...) NSLog(@"[Bypass:Hook] " fmt, ##__VA_ARGS__)

// ============================================================
// 原始方法指针
// ============================================================

static id (*orig_JSONObjectWithData)(id, SEL, NSData*, NSJSONReadingOptions, NSError**);
static id (*orig_objectForKey)(id, SEL, NSString*);
static BOOL (*orig_boolForKey)(id, SEL, NSString*);
static NSInteger (*orig_integerForKey)(id, SEL, NSString*);
static void (*orig_setObject)(id, SEL, id, NSString*);
static void (*orig_setBool)(id, SEL, BOOL, NSString*);
static void (*orig_orderFront)(id, SEL, id);
static void (*orig_makeKeyAndOrderFront)(id, SEL, id);

// ============================================================
// 工具函数
// ============================================================

static void swizzleClassMethod(Class cls, SEL sel, IMP newImp, IMP *origImp) {
    Method m = class_getClassMethod(cls, sel);
    if (m) {
        *origImp = method_getImplementation(m);
        method_setImplementation(m, newImp);
        LOG_HOOK(@"+[%@ %@]", NSStringFromClass(cls), NSStringFromSelector(sel));
    }
}

static void swizzleInstanceMethod(Class cls, SEL sel, IMP newImp, IMP *origImp) {
    Method m = class_getInstanceMethod(cls, sel);
    if (m) {
        *origImp = method_getImplementation(m);
        method_setImplementation(m, newImp);
        LOG_HOOK(@"-[%@ %@]", NSStringFromClass(cls), NSStringFromSelector(sel));
    }
}

// ============================================================
// Hook: NSJSONSerialization (修改 API 响应)
// ============================================================

static id hook_JSONObjectWithData(id self, SEL _cmd, NSData *data, NSJSONReadingOptions opt, NSError **error) {
    id result = orig_JSONObjectWithData(self, _cmd, data, opt, error);
    
    if (![result isKindOfClass:[NSDictionary class]]) return result;
    
    NSDictionary *dict = result;
    
    // 检查是否需要修改
    BOOL needsMod = (dict[@"remaining"] || dict[@"subscription_active"] || 
                     dict[@"authorized"] || dict[@"success"] || dict[@"account_id"] ||
                     dict[@"max_exports"] || dict[@"error"] ||
                     dict[@"activated"] || dict[@"activation_code"] || dict[@"valid"] ||
                     dict[@"code"] || dict[@"is_valid"]);
    
    if (!needsMod) return result;
    
    NSMutableDictionary *mod = [dict mutableCopy];
    
    // 激活码验证响应修改
    if (dict[@"activated"] != nil) mod[@"activated"] = @YES;
    if (dict[@"valid"] != nil) mod[@"valid"] = @YES;
    if (dict[@"is_valid"] != nil) mod[@"is_valid"] = @YES;
    if (dict[@"activation_code"]) mod[@"activation_code"] = @"BYPASS-ACTIVATED";
    
    // 核心字段修改
    if (dict[@"remaining"]) mod[@"remaining"] = @(kRemainingExports);
    if (dict[@"max_exports"]) mod[@"max_exports"] = @(kMaxExports);
    if (dict[@"subscription_active"] != nil) mod[@"subscription_active"] = @(kSubscriptionActive);
    if (dict[@"authorized"] != nil) mod[@"authorized"] = @YES;
    if (dict[@"account_valid_days_remaining"]) mod[@"account_valid_days_remaining"] = @(kAccountValidDays);
    if (dict[@"max_devices"]) mod[@"max_devices"] = @(kMaxDevices);
    
    // 强制成功
    mod[@"success"] = @YES;
    
    // 伪造账户信息
    if (!dict[@"account_id"]) {
        mod[@"account_id"] = @"bypass-account-001";
        mod[@"username"] = @"bypass@bypass.com";
        mod[@"email"] = @"bypass@bypass.com";
    }
    
    // 移除错误
    [mod removeObjectForKey:@"error"];
    [mod removeObjectForKey:@"message"];
    [mod removeObjectForKey:@"error_code"];
    
    LOG(@"API响应已修改: %@", [mod allKeys]);
    
    return mod;
}

// ============================================================
// Hook: NSUserDefaults (伪造本地状态 - 读取)
// ============================================================

static id hook_objectForKey(id self, SEL _cmd, NSString *key) {
    // 账户信息
    if ([key isEqualToString:@"NextFrameAccountId"]) {
        return @"bypass-account-001";
    }
    if ([key isEqualToString:@"NextFrameUsername"]) {
        return @"bypass@bypass.com";
    }
    if ([key isEqualToString:@"NextFrameAppAccountToken"]) {
        return @"bypass-token-permanent";
    }
    if ([key isEqualToString:@"NextFrameDeviceFingerprint"]) {
        id orig = orig_objectForKey(self, _cmd, key);
        return orig ?: [[NSUUID UUID] UUIDString];
    }
    
    // 登录状态相关
    if ([key containsString:@"LoggedIn"] || [key containsString:@"loggedIn"]) {
        return @YES;
    }
    
    return orig_objectForKey(self, _cmd, key);
}

static BOOL hook_boolForKey(id self, SEL _cmd, NSString *key) {
    // 激活状态
    if ([key containsString:@"activated"] || [key containsString:@"Activated"] ||
        [key containsString:@"isActivated"] || [key containsString:@"IsActivated"] ||
        [key containsString:@"activation"] || [key containsString:@"Activation"]) {
        LOG(@"boolForKey(%@) -> YES (已激活)", key);
        return YES;
    }
    
    // 登录状态
    if ([key containsString:@"isLoggedIn"] || [key containsString:@"IsLoggedIn"] ||
        [key containsString:@"loggedIn"] || [key containsString:@"LoggedIn"] ||
        [key containsString:@"hasAccount"] || [key containsString:@"HasAccount"]) {
        LOG(@"boolForKey(%@) -> YES", key);
        return YES;
    }
    
    // 订阅状态
    if ([key containsString:@"subscription"] || [key containsString:@"Subscription"] ||
        [key containsString:@"premium"] || [key containsString:@"Premium"]) {
        return YES;
    }
    
    // IAP 模式
    if ([key isEqualToString:@"useIAPKey"] || [key isEqualToString:@"UseIAPPurchase"]) {
        return YES;
    }
    
    // 需要登录/激活检查 - 返回 NO (不需要)
    if ([key containsString:@"needLogin"] || [key containsString:@"NeedLogin"] ||
        [key containsString:@"requireLogin"] || [key containsString:@"RequireLogin"] ||
        [key containsString:@"needActivation"] || [key containsString:@"NeedActivation"] ||
        [key containsString:@"showActivation"] || [key containsString:@"ShowActivation"]) {
        return NO;
    }
    
    return orig_boolForKey(self, _cmd, key);
}

static NSInteger hook_integerForKey(id self, SEL _cmd, NSString *key) {
    NSString *lowerKey = [key lowercaseString];
    if ([lowerKey containsString:@"remaining"] || [lowerKey containsString:@"exports"] ||
        [lowerKey containsString:@"credits"] || [lowerKey containsString:@"count"]) {
        return kRemainingExports;
    }
    
    if ([lowerKey containsString:@"validdays"] || [lowerKey containsString:@"valid_days"]) {
        return kAccountValidDays;
    }
    
    return orig_integerForKey(self, _cmd, key);
}

// ============================================================
// Hook: NSUserDefaults (写入 - 防止清除登录状态)
// ============================================================

static void hook_setObject(id self, SEL _cmd, id value, NSString *key) {
    // 阻止清除账户信息
    if ([key isEqualToString:@"NextFrameAccountId"] && value == nil) {
        LOG(@"阻止清除 NextFrameAccountId");
        return;
    }
    if ([key isEqualToString:@"NextFrameAppAccountToken"] && value == nil) {
        LOG(@"阻止清除 NextFrameAppAccountToken");
        return;
    }
    
    orig_setObject(self, _cmd, value, key);
}

static void hook_setBool(id self, SEL _cmd, BOOL value, NSString *key) {
    // 阻止设置登录状态为 NO
    if (([key containsString:@"LoggedIn"] || [key containsString:@"loggedIn"]) && !value) {
        LOG(@"阻止设置 %@ = NO", key);
        return;
    }
    
    orig_setBool(self, _cmd, value, key);
}

// ============================================================
// Hook: NSWindow (阻止登录窗口显示)
// ============================================================

static BOOL isLoginWindow(id window) {
    @try {
        NSString *title = [window title];
        NSString *identifier = [window identifier];
        id contentView = [window contentView];
        NSString *className = contentView ? NSStringFromClass([contentView class]) : @"";
        
        // 检查是否是登录窗口
        BOOL isLogin = NO;
        
        if (title && ([title containsString:@"Login"] || [title containsString:@"登录"] ||
                      [title containsString:@"Sign in"] || [title containsString:@"Account"])) {
            isLogin = YES;
        }
        
        if (identifier && [identifier containsString:@"login"]) {
            isLogin = YES;
        }
        
        if ([className containsString:@"AccountLogin"]) {
            isLogin = YES;
        }
        
        // 检查 window 的内容是否包含登录相关视图
        if (contentView) {
            for (id subview in [contentView subviews]) {
                NSString *subClassName = NSStringFromClass([subview class]);
                if ([subClassName containsString:@"Login"] || [subClassName containsString:@"Account"]) {
                    isLogin = YES;
                    break;
                }
            }
        }
        
        return isLogin;
    } @catch (NSException *e) {
        return NO;
    }
}

static void hook_orderFront(id self, SEL _cmd, id sender) {
    if (isLoginWindow(self)) {
        LOG(@"阻止登录窗口 orderFront: %@", [self title]);
        [self close];
        return;
    }
    orig_orderFront(self, _cmd, sender);
}

static void hook_makeKeyAndOrderFront(id self, SEL _cmd, id sender) {
    if (isLoginWindow(self)) {
        LOG(@"阻止登录窗口 makeKeyAndOrderFront: %@", [self title]);
        [self close];
        return;
    }
    orig_makeKeyAndOrderFront(self, _cmd, sender);
}

// ============================================================
// Hook: Swift 类
// ============================================================

static void hookSwiftClasses(void) {
    LOG(@"正在 Hook Swift 类...");
    
    // === ActivationCodeViewModel (激活码界面 ViewModel) ===
    Class ActivationCodeViewModel = objc_getClass("_TtC9NextFrame23ActivationCodeViewModel");
    if (ActivationCodeViewModel) {
        LOG(@"找到 ActivationCodeViewModel - 将 hook shouldDismiss 和验证方法");
        
        unsigned int methodCount = 0;
        Method *methods = class_copyMethodList(ActivationCodeViewModel, &methodCount);
        
        for (unsigned int i = 0; i < methodCount; i++) {
            SEL sel = method_getName(methods[i]);
            NSString *selName = NSStringFromSelector(sel);
            
            // Hook shouldDismiss getter - 返回 YES 强制关闭激活码界面
            if ([selName containsString:@"shouldDismiss"] && ![selName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) {
                    LOG(@"ActivationCodeViewModel.shouldDismiss -> YES (关闭激活码界面)");
                    return YES;
                });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"ActivationCodeViewModel.%@ -> YES", selName);
            }
            
            // Hook isVerifying - 返回 NO
            if ([selName containsString:@"isVerifying"] && ![selName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) { return NO; });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"ActivationCodeViewModel.%@ -> NO", selName);
            }
            
            // Hook successMessage - 返回成功消息
            if ([selName containsString:@"successMessage"] && ![selName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^id(id _self) {
                    return @"激活成功！";
                });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"ActivationCodeViewModel.%@ -> 激活成功", selName);
            }
            
            // Hook errorMessage - 返回 nil
            if ([selName containsString:@"errorMessage"] && ![selName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^id(id _self) { return nil; });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"ActivationCodeViewModel.%@ -> nil", selName);
            }
            
            // Hook verify 方法 - 直接成功
            if ([selName containsString:@"verify"] || [selName containsString:@"Verify"]) {
                LOG(@"发现验证方法: %@", selName);
            }
        }
        
        free(methods);
    } else {
        LOG(@"警告: 未找到 ActivationCodeViewModel");
    }
    
    // === AccountLoginViewModel (登录界面 ViewModel) ===
    Class AccountLoginViewModel = objc_getClass("_TtC9NextFrame21AccountLoginViewModel");
    if (AccountLoginViewModel) {
        LOG(@"找到 AccountLoginViewModel - 将 hook shouldDismiss");
        
        unsigned int methodCount = 0;
        Method *methods = class_copyMethodList(AccountLoginViewModel, &methodCount);
        
        for (unsigned int i = 0; i < methodCount; i++) {
            SEL sel = method_getName(methods[i]);
            NSString *selName = NSStringFromSelector(sel);
            
            // Hook shouldDismiss getter - 返回 YES 强制关闭登录界面
            if ([selName containsString:@"shouldDismiss"] && ![selName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) {
                    LOG(@"AccountLoginViewModel.shouldDismiss -> YES (关闭登录界面)");
                    return YES;
                });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"AccountLoginViewModel.%@ -> YES", selName);
            }
            
            // Hook isLoading - 永远返回 NO
            if ([selName containsString:@"isLoading"] && ![selName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) { return NO; });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"AccountLoginViewModel.%@ -> NO", selName);
            }
        }
        
        free(methods);
    }
    
    // === AccountManager ===
    Class AccountManager = objc_getClass("_TtC9NextFrame14AccountManager");
    if (AccountManager) {
        LOG(@"找到 AccountManager");
        
        unsigned int methodCount = 0;
        Method *methods = class_copyMethodList(AccountManager, &methodCount);
        
        for (unsigned int i = 0; i < methodCount; i++) {
            SEL sel = method_getName(methods[i]);
            NSString *selName = NSStringFromSelector(sel);
            
            // Hook isLoggedIn
            if ([selName containsString:@"isLoggedIn"]) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) {
                    return YES;
                });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"AccountManager.%@", selName);
            }
            
            // Hook logout
            if ([selName isEqualToString:@"logout"]) {
                IMP newImp = imp_implementationWithBlock(^(id _self) {
                    LOG(@"阻止 logout");
                });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"AccountManager.%@ (阻止)", selName);
            }
            
            // Hook accountInfo getter
            if ([selName containsString:@"accountInfo"] && ![selName containsString:@"set"]) {
                // 返回伪造的账户信息
                // 注意: Swift 对象比较复杂，这里可能需要调整
            }
        }
        
        free(methods);
    }
    
    // === EntitlementService ===
    Class EntitlementService = objc_getClass("_TtC9NextFrame18EntitlementService");
    if (EntitlementService) {
        LOG(@"找到 EntitlementService");
        
        unsigned int methodCount = 0;
        Method *methods = class_copyMethodList(EntitlementService, &methodCount);
        
        for (unsigned int i = 0; i < methodCount; i++) {
            SEL sel = method_getName(methods[i]);
            NSString *selName = NSStringFromSelector(sel);
            NSString *lowerName = [selName lowercaseString];
            
            // canExport
            if ([lowerName containsString:@"canexport"]) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) { return YES; });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"EntitlementService.%@", selName);
            }
            
            // remaining (getter)
            if ([lowerName containsString:@"remaining"] && ![lowerName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^NSInteger(id _self) { return kRemainingExports; });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"EntitlementService.%@", selName);
            }
            
            // subscriptionActive (getter)
            if ([lowerName containsString:@"subscriptionactive"] && ![lowerName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) { return YES; });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"EntitlementService.%@", selName);
            }
            
            // checkPermission / checkExport
            if ([lowerName containsString:@"check"] && 
                ([lowerName containsString:@"permission"] || [lowerName containsString:@"export"])) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) { return YES; });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"EntitlementService.%@", selName);
            }
        }
        
        free(methods);
    }
    
    // === PurchaseModeManager ===
    Class PurchaseModeManager = objc_getClass("_TtC9NextFrame19PurchaseModeManager");
    if (PurchaseModeManager) {
        LOG(@"找到 PurchaseModeManager");
        
        unsigned int methodCount = 0;
        Method *methods = class_copyMethodList(PurchaseModeManager, &methodCount);
        
        for (unsigned int i = 0; i < methodCount; i++) {
            SEL sel = method_getName(methods[i]);
            NSString *selName = NSStringFromSelector(sel);
            
            // useIAP
            if ([selName containsString:@"useIAP"] && ![selName containsString:@"set"]) {
                IMP newImp = imp_implementationWithBlock(^BOOL(id _self) { return YES; });
                method_setImplementation(methods[i], newImp);
                LOG_HOOK(@"PurchaseModeManager.%@", selName);
            }
        }
        
        free(methods);
    }
}

// ============================================================
// 强制登录和激活状态
// ============================================================

static void forceLoginState(void) {
    LOG(@"强制设置登录和激活状态...");
    
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    
    // 直接调用原始方法设置，避免被 Hook 拦截
    if (orig_setObject) {
        orig_setObject(defaults, @selector(setObject:forKey:), @"bypass-account-001", @"NextFrameAccountId");
        orig_setObject(defaults, @selector(setObject:forKey:), @"bypass@bypass.com", @"NextFrameUsername");
        orig_setObject(defaults, @selector(setObject:forKey:), @"bypass-token", @"NextFrameAppAccountToken");
        orig_setObject(defaults, @selector(setObject:forKey:), @"BYPASS-ACTIVATED", @"NextFrameActivationCode");
    } else {
        [defaults setObject:@"bypass-account-001" forKey:@"NextFrameAccountId"];
        [defaults setObject:@"bypass@bypass.com" forKey:@"NextFrameUsername"];
        [defaults setObject:@"bypass-token" forKey:@"NextFrameAppAccountToken"];
        [defaults setObject:@"BYPASS-ACTIVATED" forKey:@"NextFrameActivationCode"];
    }
    
    // 设置激活状态
    [defaults setBool:YES forKey:@"NextFrameIsActivated"];
    [defaults setBool:YES forKey:@"isActivated"];
    [defaults setBool:YES forKey:@"activated"];
    [defaults setBool:YES forKey:@"useIAPKey"];
    [defaults setBool:YES forKey:@"UseIAPPurchase"];
    [defaults setInteger:999999 forKey:@"NextFrameAccountId"];
    [defaults synchronize];
    
    LOG(@"✓ UserDefaults 已设置 (激活 + 登录)");
    
    // 发送激活和登录通知
    NSDictionary *userInfo = @{
        @"account_id": @"bypass-account-001",
        @"username": @"bypass@bypass.com",
        @"remaining": @(kRemainingExports),
        @"subscription_active": @YES,
        @"activated": @YES
    };
    
    [[NSNotificationCenter defaultCenter] postNotificationName:@"ActivationSuccessNotification" 
                                                        object:nil 
                                                      userInfo:userInfo];
    [[NSNotificationCenter defaultCenter] postNotificationName:@"UserDidLoginNotification" 
                                                        object:nil 
                                                      userInfo:userInfo];
    [[NSNotificationCenter defaultCenter] postNotificationName:@"AccountDidChangeNotification" 
                                                        object:nil 
                                                      userInfo:userInfo];
    
    LOG(@"✓ 已发送登录通知");
}

// ============================================================
// 延迟强化
// ============================================================

static void delayedReinforce(void) {
    // 0.5秒后 - 尽早关闭登录界面
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(0.5 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        LOG(@"延迟强化 (0.5s) - 尝试关闭登录界面...");
        
        // 遍历所有窗口，查找并关闭登录相关的 sheet
        for (NSWindow *window in [NSApp windows]) {
            @try {
                // 检查是否有附加的 sheet
                NSWindow *sheet = [window attachedSheet];
                if (sheet) {
                    NSString *sheetClassName = NSStringFromClass([sheet class]);
                    LOG(@"发现 sheet: %@", sheetClassName);
                    
                    // 关闭 sheet
                    [NSApp endSheet:sheet];
                    [sheet close];
                    LOG(@"✓ 已关闭 sheet");
                }
            } @catch (NSException *e) {
                LOG(@"遍历窗口异常: %@", e);
            }
        }
        
        // 查找并关闭所有 AccountLoginViewModel
        Class AccountLoginViewModel = objc_getClass("_TtC9NextFrame21AccountLoginViewModel");
        if (AccountLoginViewModel) {
            // 尝试通知关闭
            [[NSNotificationCenter defaultCenter] postNotificationName:@"DismissLoginViewNotification" 
                                                                object:nil];
        }
        
        hookSwiftClasses();
        forceLoginState();
    });
    
    // 1秒后
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 1 * NSEC_PER_SEC), dispatch_get_main_queue(), ^{
        LOG(@"延迟强化 (1s)...");
        hookSwiftClasses();
        forceLoginState();
    });
    
    // 3秒后再次
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 3 * NSEC_PER_SEC), dispatch_get_main_queue(), ^{
        LOG(@"延迟强化 (3s)...");
        
        // 尝试直接修改单例
        Class AccountManager = objc_getClass("_TtC9NextFrame14AccountManager");
        if (AccountManager) {
            SEL sharedSel = NSSelectorFromString(@"shared");
            if ([AccountManager respondsToSelector:sharedSel]) {
                id shared = ((id (*)(id, SEL))objc_msgSend)(AccountManager, sharedSel);
                if (shared) {
                    @try {
                        [shared setValue:@YES forKey:@"isLoggedIn"];
                        LOG(@"✓ 设置 AccountManager.shared.isLoggedIn = YES");
                    } @catch (NSException *e) {}
                    
                    @try {
                        [shared setValue:@YES forKey:@"_isLoggedIn"];
                        LOG(@"✓ 设置 AccountManager.shared._isLoggedIn = YES");
                    } @catch (NSException *e) {}
                }
            }
        }
        
        // EntitlementService
        Class EntitlementService = objc_getClass("_TtC9NextFrame18EntitlementService");
        if (EntitlementService) {
            SEL sharedSel = NSSelectorFromString(@"shared");
            if ([EntitlementService respondsToSelector:sharedSel]) {
                id shared = ((id (*)(id, SEL))objc_msgSend)(EntitlementService, sharedSel);
                if (shared) {
                    @try {
                        [shared setValue:@(kRemainingExports) forKey:@"remainingExports"];
                        [shared setValue:@(kRemainingExports) forKey:@"_remainingExports"];
                        [shared setValue:@YES forKey:@"subscriptionActive"];
                        [shared setValue:@YES forKey:@"_subscriptionActive"];
                        LOG(@"✓ 设置 EntitlementService 状态");
                    } @catch (NSException *e) {}
                }
            }
        }
    });
}

// ============================================================
// 安装所有 Hooks
// ============================================================

static void installAllHooks(void) {
    LOG(@"========================================");
    LOG(@"NextFrame Bypass V2 - 完全绕过登录");
    LOG(@"========================================");
    LOG(@"  remaining = %ld", (long)kRemainingExports);
    LOG(@"  subscription = YES");
    LOG(@"  valid_days = %ld", (long)kAccountValidDays);
    LOG(@"========================================");
    
    // 1. NSJSONSerialization
    swizzleClassMethod([NSJSONSerialization class],
                       @selector(JSONObjectWithData:options:error:),
                       (IMP)hook_JSONObjectWithData,
                       (IMP*)&orig_JSONObjectWithData);
    
    // 2. NSUserDefaults - 读取
    Class defaults = [NSUserDefaults class];
    swizzleInstanceMethod(defaults, @selector(objectForKey:), 
                          (IMP)hook_objectForKey, (IMP*)&orig_objectForKey);
    swizzleInstanceMethod(defaults, @selector(boolForKey:), 
                          (IMP)hook_boolForKey, (IMP*)&orig_boolForKey);
    swizzleInstanceMethod(defaults, @selector(integerForKey:), 
                          (IMP)hook_integerForKey, (IMP*)&orig_integerForKey);
    
    // 3. NSUserDefaults - 写入 (防止清除)
    swizzleInstanceMethod(defaults, @selector(setObject:forKey:), 
                          (IMP)hook_setObject, (IMP*)&orig_setObject);
    swizzleInstanceMethod(defaults, @selector(setBool:forKey:), 
                          (IMP)hook_setBool, (IMP*)&orig_setBool);
    
    // 4. NSWindow - 阻止登录窗口显示
    Class NSWindowClass = objc_getClass("NSWindow");
    if (NSWindowClass) {
        swizzleInstanceMethod(NSWindowClass, @selector(orderFront:),
                              (IMP)hook_orderFront, (IMP*)&orig_orderFront);
        swizzleInstanceMethod(NSWindowClass, @selector(makeKeyAndOrderFront:),
                              (IMP)hook_makeKeyAndOrderFront, (IMP*)&orig_makeKeyAndOrderFront);
        LOG(@"✓ NSWindow hooks 已安装");
    }
    
    // 5. Swift 类
    hookSwiftClasses();
    
    // 6. 强制登录
    forceLoginState();
    
    LOG(@"========================================");
    LOG(@"所有 Hooks 已安装!");
    LOG(@"========================================");
}

// ============================================================
// 构造函数
// ============================================================

__attribute__((constructor))
static void initialize(void) {
    @autoreleasepool {
        NSString *process = [[NSProcessInfo processInfo] processName];
        LOG(@"Dylib 加载: %@", process);
        
        if ([process containsString:@"NextFrame"]) {
            installAllHooks();
            delayedReinforce();
        }
    }
}

__attribute__((destructor))
static void cleanup(void) {
    LOG(@"Dylib 卸载");
}
